import argparse
from pathlib import Path
import cv2
import pandas as pd
from ultralytics import YOLO


FINAL_CLASSES = {
    0: "person",
    1: "helmet",
    2: "no_helmet",
    3: "vest",
    4: "no_vest",
    5: "gloves",
    6: "goggles",
    7: "boots"
}


def compute_iou(box_a, box_b):
    ax1, ay1, ax2, ay2 = box_a
    bx1, by1, bx2, by2 = box_b

    inter_x1 = max(ax1, bx1)
    inter_y1 = max(ay1, by1)
    inter_x2 = min(ax2, bx2)
    inter_y2 = min(ay2, by2)

    inter_w = max(0, inter_x2 - inter_x1)
    inter_h = max(0, inter_y2 - inter_y1)

    inter_area = inter_w * inter_h

    area_a = max(0, ax2 - ax1) * max(0, ay2 - ay1)
    area_b = max(0, bx2 - bx1) * max(0, by2 - by1)

    union_area = area_a + area_b - inter_area

    if union_area == 0:
        return 0.0

    return inter_area / union_area


def expand_box(box, image_shape, scale_x=0.20, scale_y=0.15):
    h, w = image_shape[:2]
    x1, y1, x2, y2 = box

    bw = x2 - x1
    bh = y2 - y1

    nx1 = max(0, int(x1 - bw * scale_x))
    ny1 = max(0, int(y1 - bh * scale_y))
    nx2 = min(w - 1, int(x2 + bw * scale_x))
    ny2 = min(h - 1, int(y2 + bh * scale_y))

    return [nx1, ny1, nx2, ny2]


def box_center(box):
    x1, y1, x2, y2 = box
    return [(x1 + x2) / 2, (y1 + y2) / 2]


def point_inside_box(point, box):
    px, py = point
    x1, y1, x2, y2 = box
    return x1 <= px <= x2 and y1 <= py <= y2


def extract_person_detections(result, conf_threshold=0.25):
    detections = []

    if result.boxes is None:
        return detections

    for box in result.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])

        # En COCO, la clase 0 corresponde a person.
        if cls_id != 0 or conf < conf_threshold:
            continue

        xyxy = box.xyxy[0].cpu().numpy().astype(int).tolist()

        detections.append({
            "class_name": "person",
            "confidence": conf,
            "box": xyxy
        })

    return detections


def extract_ppe_detections(result, conf_threshold=0.15):
    detections = []

    if result.boxes is None:
        return detections

    for box in result.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])

        if conf < conf_threshold:
            continue

        class_name = FINAL_CLASSES.get(cls_id, str(cls_id))
        xyxy = box.xyxy[0].cpu().numpy().astype(int).tolist()

        detections.append({
            "class_name": class_name,
            "confidence": conf,
            "box": xyxy
        })

    return detections


def associate_ppe_to_person(person_box, ppe_detections, image_shape):
    expanded_person_box = expand_box(person_box, image_shape)
    associated = []

    for det in ppe_detections:
        ppe_box = det["box"]
        center = box_center(ppe_box)
        center_inside = point_inside_box(center, expanded_person_box)
        iou_value = compute_iou(expanded_person_box, ppe_box)

        if center_inside or iou_value > 0.01:
            associated.append(det)

    return associated


def get_best_conf(associated_ppe, class_name):
    confs = [
        det["confidence"]
        for det in associated_ppe
        if det["class_name"] == class_name
    ]

    if not confs:
        return 0.0

    return max(confs)


def evaluate_compliance_v3(associated_ppe):
    helmet_conf = get_best_conf(associated_ppe, "helmet")
    no_helmet_conf = get_best_conf(associated_ppe, "no_helmet")

    vest_conf = get_best_conf(associated_ppe, "vest")
    no_vest_conf = get_best_conf(associated_ppe, "no_vest")

    has_helmet = helmet_conf > 0 and helmet_conf >= no_helmet_conf
    has_no_helmet = no_helmet_conf > 0 and no_helmet_conf > helmet_conf

    has_vest = vest_conf > 0 and vest_conf >= no_vest_conf
    has_no_vest = no_vest_conf > 0 and no_vest_conf > vest_conf

    if has_helmet:
        casco_status = "cumple_casco"
    elif has_no_helmet:
        casco_status = "no_cumple_casco"
    else:
        casco_status = "revision_casco"

    if has_no_helmet or has_no_vest:
        full_status = "no_cumple"
    elif has_helmet and has_vest:
        full_status = "cumple"
    else:
        full_status = "revision"

    return casco_status, full_status


def draw_results(image, compliance_results, ppe_detections):
    output = image.copy()

    for det in ppe_detections:
        x1, y1, x2, y2 = det["box"]
        label = f'{det["class_name"]} {det["confidence"]:.2f}'

        cv2.rectangle(output, (x1, y1), (x2, y2), (255, 255, 0), 2)
        cv2.putText(
            output,
            label,
            (x1, max(20, y1 - 5)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 0),
            2
        )

    for result in compliance_results:
        x1, y1, x2, y2 = result["person_box"]

        if result["full_status"] == "cumple":
            color = (0, 255, 0)
            label = "CUMPLE"
        elif result["full_status"] == "no_cumple":
            color = (0, 0, 255)
            label = "NO CUMPLE"
        else:
            color = (0, 165, 255)
            label = "REVISION"

        cv2.rectangle(output, (x1, y1), (x2, y2), color, 3)
        cv2.putText(
            output,
            label,
            (x1, max(25, y1 - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

    total_people = len(compliance_results)
    casco_ok = sum(1 for r in compliance_results if r["casco_status"] == "cumple_casco")
    full_ok = sum(1 for r in compliance_results if r["full_status"] == "cumple")

    tasa_casco = casco_ok / total_people if total_people > 0 else 0
    tasa_completo = full_ok / total_people if total_people > 0 else 0

    summary_text = f"Casco: {tasa_casco:.2%} | Completo: {tasa_completo:.2%}"

    cv2.putText(
        output,
        summary_text,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (255, 255, 255),
        3
    )

    return output


def process_image(image_path, person_model, ppe_model, output_dir, conf_person, conf_ppe):
    image = cv2.imread(str(image_path))

    if image is None:
        print(f"No se pudo leer la imagen: {image_path}")
        return None

    person_result = person_model.predict(
        source=str(image_path),
        imgsz=640,
        conf=conf_person,
        verbose=False
    )[0]

    ppe_result = ppe_model.predict(
        source=str(image_path),
        imgsz=640,
        conf=conf_ppe,
        verbose=False
    )[0]

    person_detections = extract_person_detections(person_result, conf_person)
    ppe_detections = extract_ppe_detections(ppe_result, conf_ppe)

    compliance_results = []

    for person in person_detections:
        associated_ppe = associate_ppe_to_person(
            person["box"],
            ppe_detections,
            image.shape
        )

        casco_status, full_status = evaluate_compliance_v3(associated_ppe)

        compliance_results.append({
            "person_box": person["box"],
            "casco_status": casco_status,
            "full_status": full_status,
            "associated_ppe": [det["class_name"] for det in associated_ppe]
        })

    total_people = len(compliance_results)
    casco_ok = sum(1 for r in compliance_results if r["casco_status"] == "cumple_casco")
    full_ok = sum(1 for r in compliance_results if r["full_status"] == "cumple")
    revision = sum(1 for r in compliance_results if r["full_status"] == "revision")
    no_cumple = sum(1 for r in compliance_results if r["full_status"] == "no_cumple")

    tasa_casco = casco_ok / total_people if total_people > 0 else 0
    tasa_completo = full_ok / total_people if total_people > 0 else 0

    output_image = draw_results(image, compliance_results, ppe_detections)

    output_path = output_dir / f"resultado_{image_path.stem}.jpg"
    cv2.imwrite(str(output_path), output_image)

    return {
        "imagen": image_path.name,
        "personas_detectadas": total_people,
        "cumplen_casco": casco_ok,
        "cumplen_completo": full_ok,
        "no_cumplen": no_cumple,
        "revision": revision,
        "tasa_casco": tasa_casco,
        "tasa_cumplimiento_completo": tasa_completo,
        "output": str(output_path)
    }


def run_demo(args):
    input_dir = Path(args.input)
    output_dir = Path(args.output)
    weights_path = Path(args.weights)

    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_dir.exists():
        raise FileNotFoundError(f"No existe la carpeta de imágenes: {input_dir}")

    if not weights_path.exists():
        raise FileNotFoundError(
            f"No se encontró el modelo entrenado: {weights_path}. "
            "Descarga best.pt y colócalo en la carpeta weights/."
        )

    print("Cargando detector auxiliar de personas YOLOv8 COCO...")
    person_model = YOLO("yolov8s.pt")

    print("Cargando modelo PPE entrenado...")
    ppe_model = YOLO(str(weights_path))

    image_files = []
    for ext in ["*.jpg", "*.jpeg", "*.png"]:
        image_files.extend(input_dir.glob(ext))

    image_files = sorted(image_files)

    if not image_files:
        raise FileNotFoundError(f"No se encontraron imágenes en: {input_dir}")

    print(f"Imágenes encontradas: {len(image_files)}")

    rows = []

    for image_path in image_files:
        print(f"Procesando: {image_path.name}")
        result = process_image(
            image_path=image_path,
            person_model=person_model,
            ppe_model=ppe_model,
            output_dir=output_dir,
            conf_person=args.conf_person,
            conf_ppe=args.conf_ppe
        )

        if result is not None:
            rows.append(result)

    summary_df = pd.DataFrame(rows)
    summary_path = output_dir / "resumen_cumplimiento.csv"
    summary_df.to_csv(summary_path, index=False)

    print("\nProceso finalizado.")
    print(f"Imágenes anotadas guardadas en: {output_dir}")
    print(f"Resumen CSV guardado en: {summary_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Pipeline de detección de cumplimiento de EPP con YOLOv8."
    )

    parser.add_argument(
        "--mode",
        type=str,
        default="demo",
        choices=["demo"],
        help="Modo de ejecución. Actualmente se soporta demo."
    )

    parser.add_argument(
        "--input",
        type=str,
        default="data/demo_images",
        help="Carpeta con imágenes de entrada."
    )

    parser.add_argument(
        "--output",
        type=str,
        default="results/demo_outputs",
        help="Carpeta donde se guardarán las imágenes anotadas y el CSV."
    )

    parser.add_argument(
        "--weights",
        type=str,
        default="weights/best.pt",
        help="Ruta al modelo PPE entrenado."
    )

    parser.add_argument(
        "--conf-person",
        type=float,
        default=0.25,
        help="Umbral de confianza para detección de personas."
    )

    parser.add_argument(
        "--conf-ppe",
        type=float,
        default=0.15,
        help="Umbral de confianza para detección de EPP."
    )

    args = parser.parse_args()

    if args.mode == "demo":
        run_demo(args)


if __name__ == "__main__":
    main()
