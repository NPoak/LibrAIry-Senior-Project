from fastapi import FastAPI, Request
from sentence_transformers import SentenceTransformer
import torch

app = FastAPI()

# 1. GPU Setup
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"🚀 Loading model on device: {device}")

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
# Load model to GPU
encoder = SentenceTransformer(MODEL_NAME, device=device)

@app.post("/bookembed")
async def embed_items(request: Request):
    # Get input data from n8n HTTP Request
    input_data = await request.json()
    
    # Ensure it's a list to match your original loop logic
    items = input_data if isinstance(input_data, list) else [input_data]
    
    output_items = []

    for item in items:
        try:
            # Extract fields
            title = item.get('title', '') or ""
            author = item.get('author', '') or ""
            publisher = item.get('publisher', '') or ""
            description = item.get('description', '') or ""
            reason = item.get('reason', '') or item.get('specify_reason', '') or ""

            # --- YOUR EXACT LOGIC START ---
            parts = [
                f"Title: {title}",
                f"Author: {author}" if author else "",
                f"Publisher: {publisher}" if publisher else "",
                f"User Context: {reason}" if reason else "",
                f"Description: {description}" if description else ""
            ]
            text_to_embed = ". ".join([p for p in parts if p != ""])

            if text_to_embed:
                # Encode on GPU
                embedding = encoder.encode(text_to_embed)
                vector_list = embedding.tolist()

                # Your specific string formatting
                vector_str_format = str(vector_list).replace(" ", "")

                # --- จุดที่แก้ไข (ใช้ .copy() เพื่อรักษา ID) ---
                result_item = item.copy()  # <--- Copy request_id, batch_id ติดมาด้วย
                
                result_item.update({
                    "combined_text_used": text_to_embed,
                    "vector": vector_list,
                    "vector_text": vector_str_format,
                    "dimension": len(vector_list)
                })

                output_items.append(result_item)
            else:
                # กรณี Error ก็ส่ง ID กลับไปด้วย (เผื่อเอาไปเช็ค)
                error_item = item.copy()
                error_item["error"] = "No content to embed"
                output_items.append(error_item)
            # --- YOUR EXACT LOGIC END ---

        except Exception as e:
            error_item = item.copy()
            error_item["error"] = str(e)
            output_items.append(error_item)

    return output_items

@app.post("/facultyembed")
async def faculty_embed(request: Request):
    # รับ Data จาก n8n
    input_data = await request.json()
    
    # แปลงให้เป็น List เสมอ (เผื่อส่งมาตัวเดียว)
    items = input_data if isinstance(input_data, list) else [input_data]
    output_items = []

    for item in items:
        try:
            # 1. ดึงข้อมูล (ใช้ .get เพื่อกัน Error ถ้า field ไม่มี)
            # หมายเหตุ: เราไม่ดึง ID มาใส่ในตัวแปร text เพื่อป้องกัน Noise ในการทำ Vector
            facultyNameTH = item.get('FacultyNameTH', '') or ""
            facultyNameEN = item.get('FacultyNameEN', '') or ""
            facultyDescriptionTH = item.get('FacultyDescriptionTH', '') or ""
            facultyDescriptionEN = item.get('FacultyDescriptionEN', '') or ""

            # 2. สร้าง Text สำหรับ Embed (เฉพาะเนื้อหาที่สำคัญ)
            parts = [
                f"FacultyNameTH: {facultyNameTH}" if facultyNameTH else "",
                f"FacultyNameEN: {facultyNameEN}" if facultyNameEN else "",
                f"FacultyDescriptionTH: {facultyDescriptionTH}" if facultyDescriptionTH else "",
                f"FacultyDescriptionEN: {facultyDescriptionEN}" if facultyDescriptionEN else "",
            ]
            # รวม Text ตัดช่องว่างทิ้ง
            text_to_embed = ". ".join([p for p in parts if p != ""])

            if text_to_embed:
                # 3. ทำ Embedding
                embedding = encoder.encode(text_to_embed)
                vector_list = embedding.tolist()
                # จัด Format String สำหรับ Postgres Vector (ถ้าจำเป็นต้องใช้ String)
                vector_str_format = str(vector_list).replace(" ", "")

                # 4. สร้าง Output (จุดสำคัญ!)
                # COPY ข้อมูลต้นฉบับทั้งหมด (รวม ID ที่ส่งมาจาก n8n) มาใส่ตัวแปรใหม่ก่อน
                result_item = item.copy() 
                
                # แล้วค่อย Update Vector ใส่เพิ่มเข้าไป
                result_item.update({
                    "combined_text_used": text_to_embed, # ส่งกลับไปดูได้ว่าเอาอะไรไป embed
                    "vector": vector_list,               # เป็น Array (ใช้กับ Postgres Node)
                    "vector_text": vector_str_format,    # เป็น String (เผื่อต้องใช้ cast)
                    "dimension": len(vector_list)
                })
                
                output_items.append(result_item)
            else:
                # กรณีไม่มีเนื้อหาให้ Embed ก็ส่งคืนของเดิมพร้อม Error
                err_item = item.copy()
                err_item["error"] = "No content to embed (fields are empty)"
                output_items.append(err_item)

        except Exception as e:
            # กรณีเกิด Error อื่นๆ
            err_item = item.copy()
            err_item["error"] = str(e)
            output_items.append(err_item)
    
    return output_items

@app.post("/departmentembed")
async def department_embed(request: Request):
    input_data = await request.json()
    items = input_data if isinstance(input_data, list) else [input_data]
    output_items = []

    for item in items:
        try:
            # 1. ดึงข้อมูล
            degree = item.get('Degree', '') or ""
            DepartmentNameTH = item.get('DepartmentNameTH', '') or ""
            DepartmentNameEN = item.get('DepartmentNameEN', '') or ""
            DepartmentDescriptionTH = item.get('DepartmentDescriptionTH', '') or ""
            DepartmentDescriptionEN = item.get('DepartmentDescriptionEN', '') or ""

            # 2. สร้าง Text (เน้นเนื้อหา ไม่เอา ID)
            parts = [
                f"DepartmentNameTH: {DepartmentNameTH}" if DepartmentNameTH else "",
                f"DepartmentNameEN: {DepartmentNameEN}" if DepartmentNameEN else "",
                f"DepartmentDescriptionTH: {DepartmentDescriptionTH}" if DepartmentDescriptionTH else "",
                f"DepartmentDescriptionEN: {DepartmentDescriptionEN}" if DepartmentDescriptionEN else "",
                f"Degree: {degree}" if degree else ""
            ]
            text_to_embed = ". ".join([p for p in parts if p != ""])

            if text_to_embed:
                # 3. ทำ Embedding
                embedding = encoder.encode(text_to_embed)
                vector_list = embedding.tolist()
                vector_str_format = str(vector_list).replace(" ", "")

                # 4. สร้าง Output (Pass-through ID)
                result_item = item.copy() # <--- จุดสำคัญ: Copy ID ที่ส่งมาติดไปด้วย
                
                result_item.update({
                    "combined_text_used": text_to_embed,
                    "vector": vector_list,
                    "vector_text": vector_str_format,
                    "dimension": len(vector_list)
                })

                output_items.append(result_item)
            else:
                err_item = item.copy()
                err_item["error"] = "No content to embed"
                output_items.append(err_item)

        except Exception as e:
            err_item = item.copy()
            err_item["error"] = str(e)
            output_items.append(err_item)
    
    return output_items
# @app.post("/facultyembed")
# async def faculty_embed(request: Request):
#     # Get input data from n8n HTTP Request
#     input_data = await request.json()

#     # Ensure it's a list to match your original loop logic
#     items = input_data if isinstance(input_data, list) else [input_data]

#     output_items = []

#     for item in items:
#         try:
#             # Extract fields
#             # Note: Direct JSON input uses .get(), not .json.get()
#             facultyNameTH = item.get('FacultyNameTH', '') or ""
#             facultyNameEN = item.get('FacultyNameEN', '') or ""
#             facultyDescriptionTH = item.get('FacultyDescriptionTH', '') or ""
#             facultyDescriptionEN = item.get('FacultyDescriptionEN', '') or ""

#             parts = [
#                 f"facultyNameTH: {facultyNameTH}",
#                 f"facultyNameEN: {facultyNameEN}",
#                 f"facultyDescriptionTH: {facultyDescriptionTH}" if facultyDescriptionTH else "",
#                 f"facultyDescriptionEN: {facultyDescriptionEN}" if facultyDescriptionEN else "",
#             ]

#             text_to_embed = ". ".join([p for p in parts if p != ""])

#             if text_to_embed:
#                 # Encode on GPU
#                 embedding = encoder.encode(text_to_embed)
#                 vector_list = embedding.tolist()

#                 # Your specific string formatting
#                 vector_str_format = str(vector_list).replace(" ", "")

#                 output_items.append({
#                     "facultyNameTH": facultyNameTH,
#                     "facultyNameEN": facultyNameEN,
#                     "facultyDescriptionTH": facultyDescriptionTH,
#                     "facultyDescriptionEN": facultyDescriptionEN,
#                     "combined_text_used": text_to_embed,
#                     "vector": vector_list,
#                     "vector_text": vector_str_format,
#                     "dimension": len(vector_list)
#                 })
#             else:
#                 output_items.append({"error": "No content to embed", "facultyName": facultyName})

#         except:
#             output_items.append({
#                 "error": str(e),
#                 "facultyName": item.get('facultyName')
#             })
    
#     return output_items


# @app.post("/departmentembed")
# async def faculty_embed(request: Request):
#     # Get input data from n8n HTTP Request
#     input_data = await request.json()

#     # Ensure it's a list to match your original loop logic
#     items = input_data if isinstance(input_data, list) else [input_data]

#     output_items = []

#     for item in items:
#         try:
#             # Extract fields
#             # Note: Direct JSON input uses .get(), not .json.get()
#             degree = item.get('Degree', '') or ""
#             DepartmentNameTH = item.get('DepartmentNameTH', '') or ""
#             DepartmentNameEN = item.get('DepartmentNameEN', '') or ""
#             DepartmentDescriptionTH = item.get('DepartmentDescriptionTH', '') or ""
#             DepartmentDescriptionEN = item.get('DepartmentDescriptionEN', '') or ""

#             parts = [
#                 f"DepartmentNameTH: {DepartmentNameTH}",
#                 f"DepartmentNameEN: {DepartmentNameEN}",
#                 f"DepartmentDescriptionTH: {DepartmentDescriptionTH}" if DepartmentDescriptionTH else "",
#                 f"DepartmentDescriptionEN: {DepartmentDescriptionEN}" if DepartmentDescriptionEN else "",
#                 f"Degree: {degree}" if degree else ""
#             ]

#             text_to_embed = ". ".join([p for p in parts if p != ""])

#             if text_to_embed:
#                 # Encode on GPU
#                 embedding = encoder.encode(text_to_embed)
#                 vector_list = embedding.tolist()

#                 # Your specific string formatting
#                 vector_str_format = str(vector_list).replace(" ", "")

#                 output_items.append({
#                     "DepartmentNameTH": DepartmentNameTH,
#                     "DepartmentNameEN": DepartmentNameEN,
#                     "DepartmentDescriptionTH": DepartmentDescriptionTH,
#                     "DepartmentDescriptionEN": DepartmentDescriptionEN,
#                     "Degree": degree,
#                     "combined_text_used": text_to_embed,
#                     "vector": vector_list,
#                     "vector_text": vector_str_format,
#                     "dimension": len(vector_list)
#                 })
#             else:
#                 output_items.append({"error": "No content to embed", "DepartmentName": DepartmentName})

#         except:
#             output_items.append({
#                 "error": str(e),
#                 "DepartmentName": item.get('DepartmentName')
#             })
    
#     return output_items