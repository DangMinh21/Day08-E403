# PLAN — Day 08 Lab (RAG Pipeline)

Muc tieu: hoan thanh lab end-to-end theo dung thu tu, co scorecard baseline/variant va docs day du de nop.

## 1. Chuan bi moi truong

- [ ] Vao dung thu muc lab:
  - `cd day08/lab`
- [ ] Cai dependencies:
  - `pip install -r requirements.txt`
- [ ] Tao `.env` tu mau:
  - `cp .env.example .env`
- [ ] Dien API key va chon stack:
  - Khuyen nghi nhanh: `LLM_PROVIDER=openai`, `EMBEDDING_PROVIDER=openai`
- [ ] Chay test setup ban dau:
  - `python index.py`

Definition of Done:
- Script chay duoc den phan preview chunk, khong loi import.

---

## 2. Sprint 1 — Hoan thien Indexing (`index.py`)

### 2.1 Implement bat buoc

- [ ] Implement `get_embedding()`:
  - Lua chon OpenAI hoac Sentence Transformers.
- [ ] Implement `build_index()`:
  - Khoi tao ChromaDB `PersistentClient`
  - Tao/get collection `rag_lab`
  - Doc tung file trong `data/docs/*.txt`
  - `preprocess_document()` -> `chunk_document()`
  - Embed tung chunk va `upsert` vao Chroma

### 2.2 Kiem tra chat luong index

- [ ] Bat `build_index()` trong `if __name__ == "__main__":`
- [ ] Chay:
  - `python index.py`
- [ ] Bat va chay:
  - `list_chunks()`
  - `inspect_metadata_coverage()`

Definition of Done:
- Index du 5 tai lieu.
- Moi chunk co metadata toi thieu: `source`, `section`, `effective_date`.
- Chunk khong cat vo nghia giua dieu khoan.

---

## 3. Sprint 2 — Baseline RAG (`rag_answer.py`)

### 3.1 Implement bat buoc

- [ ] Implement `retrieve_dense()`:
  - Embed query
  - Query ChromaDB
  - Convert `distance` thanh `score` (`score = 1 - distance`)
- [ ] Implement `call_llm()`:
  - Doc provider tu `.env`
  - Goi model voi `temperature=0`
- [ ] Dam bao output `rag_answer()` co:
  - `answer`
  - `sources`
  - `chunks_used`

### 3.2 Kiem thu baseline

- [ ] Chay:
  - `python rag_answer.py`
- [ ] Test toi thieu cac cau:
  - SLA P1
  - Refund 7 ngay
  - Level 3 approval
  - Query khong co du lieu (`ERR-403-AUTH`)

Definition of Done:
- Cac cau co du lieu tra loi dung huong va co citation.
- Cau thieu du lieu tra loi abstain (khong bia).

---

## 4. Sprint 3 — Tuning 1 bien (khuyen nghi Hybrid)

### 4.1 Chon bien tuning (A/B Rule)

- [ ] Chi doi 1 bien duy nhat.
- [ ] Khuyen nghi cho bo du lieu nay: `hybrid retrieval`.

### 4.2 Implement variant

- [ ] Implement `retrieve_sparse()` bang BM25.
- [ ] Implement `retrieve_hybrid()` bang RRF:
  - `RRF = w_dense * 1/(60 + rank_dense) + w_sparse * 1/(60 + rank_sparse)`
- [ ] (Optional) Implement `rerank()` neu con thoi gian.

### 4.3 Danh gia nhanh variant

- [ ] Chay `compare_retrieval_strategies()` voi query kho:
  - alias: "Approval Matrix ..."
  - query thieu context
  - query co nhieu chi tiet

Definition of Done:
- Variant chay duoc end-to-end.
- Co bang chung variant cai thien it nhat 1-2 query kho.

---

## 5. Sprint 4 — Evaluation & Scorecard (`eval.py`)

### 5.1 Chuan hoa config

- [ ] Cap nhat `BASELINE_CONFIG` va `VARIANT_CONFIG` dung voi code da implement.

### 5.2 Hoan thien scoring

- [ ] Implement toi thieu cac ham:
  - `score_faithfulness()`
  - `score_answer_relevance()`
  - `score_completeness()`
- [ ] Neu chua tu dong hoa, cham thu cong nhung phai co `notes` ro rang.

### 5.3 Chay scorecard

- [ ] Chay baseline:
  - `run_scorecard(BASELINE_CONFIG)`
- [ ] Chay variant:
  - `run_scorecard(VARIANT_CONFIG)`
- [ ] Chay A/B:
  - `compare_ab(...)`
- [ ] Dam bao sinh file:
  - `results/scorecard_baseline.md`
  - `results/scorecard_variant.md`
  - `results/ab_comparison.csv` (neu bat export)

Definition of Done:
- Co so lieu thuc cho baseline va variant.
- Co delta ro rang va giai thich duoc tai sao.

---

## 6. Hoan thien tai lieu nop bai

### 6.1 `docs/architecture.md`

- [ ] Dien tong quan he thong (2-3 cau).
- [ ] Dien bang chunking decision (size, overlap, strategy, ly do).
- [ ] Dien retrieval baseline + variant.
- [ ] Dien LLM/embedding config.
- [ ] Cap nhat failure mode checklist theo nhung loi gap thuc te.

### 6.2 `docs/tuning-log.md`

- [ ] Dien baseline metrics.
- [ ] Dien 1 bien thay doi cho Variant 1.
- [ ] Dien bang delta baseline vs variant.
- [ ] Viet ket luan co evidence theo tung query.

Definition of Done:
- Khong con `TODO` o cac muc chinh.
- Doc lai thay ro quyet dinh ky thuat va ket qua.

---

## 7. Dry-run cuoi truoc khi nop

- [ ] Chay full flow:
  - `python index.py`
  - `python rag_answer.py`
  - `python eval.py`
- [ ] Kiem tra artifacts:
  - Code chay duoc
  - Co scorecard baseline + variant
  - Docs day du

Checklist pass cuoi:
- [ ] Khong crash.
- [ ] Khong hallucination o cau khong du context.
- [ ] Citation/sources xuat hien o cau co du lieu.
- [ ] A/B chi doi 1 bien va co giai thich ro.

---

## 8. Thu tu thuc hien toi uu theo thoi gian (goi y)

1. Setup + Sprint 1 (index)  
2. Sprint 2 (dense + llm)  
3. Sprint 3 (hybrid)  
4. Sprint 4 (scorecard + A/B)  
5. Dien docs + dry-run + nop

---

## 9. Risk canh bao (de tranh mat diem)

- Khong de `NotImplementedError` trong cac ham core.
- Khong doi nhieu bien cung luc khi A/B.
- Khong bo qua query abstain (day la diem phat nang neu bia).
- Khong quen tao output trong `results/`.

