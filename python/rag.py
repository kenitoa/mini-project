"""
RAG (Retrieval-Augmented Generation) 알고리즘 흐름도 구현
==========================================================

전체 흐름:
    ┌──────────────────────────────────────────────────────────────┐
    │                      [인덱싱(Indexing) 단계]                  │
    │                                                              │
    │   1) 문서 로드(Load)                                          │
    │           │                                                  │
    │           ▼                                                  │
    │   2) 청크 분할(Split / Chunking)                              │
    │           │                                                  │
    │           ▼                                                  │
    │   3) 임베딩(Embedding) 생성                                   │
    │           │                                                  │
    │           ▼                                                  │
    │   4) 벡터 저장소(Vector Store)에 저장                         │
    └──────────────────────────────────────────────────────────────┘
                              │
                              ▼
    ┌──────────────────────────────────────────────────────────────┐
    │                  [질의(Query / Runtime) 단계]                 │
    │                                                              │
    │   5) 사용자 질문(Query) 입력                                  │
    │           │                                                  │
    │           ▼                                                  │
    │   6) 질문 임베딩(Query Embedding)                             │
    │           │                                                  │
    │           ▼                                                  │
    │   7) 유사도 검색(Retrieval, Top-K)                            │
    │           │                                                  │
    │           ▼                                                  │
    │   8) 프롬프트 증강(Context Augmentation)                      │
    │           │                                                  │
    │           ▼                                                  │
    │   9) LLM 생성(Generation)                                     │
    │           │                                                  │
    │           ▼                                                  │
    │  10) 최종 답변(Answer) 반환                                   │
    └──────────────────────────────────────────────────────────────┘

본 파일은 외부 라이브러리 없이(파이썬 표준 라이브러리만 사용) 위 흐름을
교육용으로 단순화하여 구현한 예시이다.
실제 프로덕션에서는 임베딩 모델(OpenAI, SentenceTransformers 등)과
벡터 DB(FAISS, Chroma, Pinecone 등), LLM(GPT, Claude 등)을 연결한다.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Iterable


# ---------------------------------------------------------------------------
# 1) 문서 로드 (Load)
# ---------------------------------------------------------------------------
def load_documents() -> list[str]:
    """예시 문서를 반환한다. 실제로는 파일/DB/웹에서 읽어온다."""
    return [
        "파이썬은 1991년 귀도 반 로섬이 발표한 고수준 프로그래밍 언어이다. "
        "동적 타이핑과 가독성이 뛰어난 문법을 특징으로 한다.",

        "RAG는 Retrieval-Augmented Generation의 약자로, "
        "검색을 통해 외부 지식을 가져와 LLM의 답변에 활용하는 기법이다. "
        "환각(hallucination)을 줄이고 최신 정보를 반영하는 데 유용하다.",

        "벡터 데이터베이스는 임베딩 벡터를 저장하고 코사인 유사도 등으로 "
        "유사한 항목을 빠르게 검색할 수 있도록 설계된 데이터베이스이다. "
        "대표적으로 FAISS, Chroma, Pinecone, Weaviate 등이 있다.",

        "임베딩이란 텍스트, 이미지 같은 비정형 데이터를 의미를 보존한 채 "
        "고정 길이의 실수 벡터로 변환하는 과정을 말한다.",

        "프롬프트 엔지니어링은 LLM에게 원하는 결과를 얻기 위해 "
        "입력 프롬프트를 설계하고 최적화하는 작업이다.",
    ]


# ---------------------------------------------------------------------------
# 2) 청크 분할 (Split / Chunking)
# ---------------------------------------------------------------------------
@dataclass
class Chunk:
    doc_id: int
    chunk_id: int
    text: str


def split_into_chunks(documents: list[str], chunk_size: int = 60,
                      overlap: int = 10) -> list[Chunk]:
    """문자 단위로 슬라이딩 윈도우 청킹을 수행한다."""
    chunks: list[Chunk] = []
    for doc_id, doc in enumerate(documents):
        start = 0
        cid = 0
        step = max(1, chunk_size - overlap)
        while start < len(doc):
            piece = doc[start:start + chunk_size].strip()
            if piece:
                chunks.append(Chunk(doc_id=doc_id, chunk_id=cid, text=piece))
                cid += 1
            start += step
    return chunks


# ---------------------------------------------------------------------------
# 3) 임베딩 생성 (Embedding)
#    - 데모용으로 TF(Bag-of-Words) 기반의 sparse 벡터를 만든다.
#    - 실제로는 sentence-transformers, OpenAI Embeddings 등을 사용한다.
# ---------------------------------------------------------------------------
_TOKEN_RE = re.compile(r"[A-Za-z0-9가-힣]+")


def tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


def embed(text: str) -> dict[str, float]:
    """단순 TF 임베딩(희소 벡터를 dict로 표현)."""
    tokens = tokenize(text)
    if not tokens:
        return {}
    counts = Counter(tokens)
    total = sum(counts.values())
    return {tok: cnt / total for tok, cnt in counts.items()}


# ---------------------------------------------------------------------------
# 4) 벡터 저장소 (Vector Store)
# ---------------------------------------------------------------------------
@dataclass
class VectorStore:
    chunks: list[Chunk] = field(default_factory=list)
    vectors: list[dict[str, float]] = field(default_factory=list)

    def add(self, chunk: Chunk, vector: dict[str, float]) -> None:
        self.chunks.append(chunk)
        self.vectors.append(vector)

    @staticmethod
    def cosine_similarity(a: dict[str, float], b: dict[str, float]) -> float:
        if not a or not b:
            return 0.0
        # 더 짧은 쪽을 기준으로 내적 계산
        if len(a) > len(b):
            a, b = b, a
        dot = sum(v * b.get(k, 0.0) for k, v in a.items())
        norm_a = math.sqrt(sum(v * v for v in a.values()))
        norm_b = math.sqrt(sum(v * v for v in b.values()))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    def search(self, query_vec: dict[str, float], top_k: int = 3
               ) -> list[tuple[float, Chunk]]:
        scored = [
            (self.cosine_similarity(query_vec, vec), chunk)
            for vec, chunk in zip(self.vectors, self.chunks)
        ]
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:top_k]


def build_vector_store(chunks: Iterable[Chunk]) -> VectorStore:
    store = VectorStore()
    for chunk in chunks:
        store.add(chunk, embed(chunk.text))
    return store


# ---------------------------------------------------------------------------
# 5~7) 질문 입력 → 임베딩 → 검색 (Retrieval)
# ---------------------------------------------------------------------------
def retrieve(store: VectorStore, query: str, top_k: int = 3
             ) -> list[tuple[float, Chunk]]:
    query_vec = embed(query)
    return store.search(query_vec, top_k=top_k)


# ---------------------------------------------------------------------------
# 8) 프롬프트 증강 (Context Augmentation)
# ---------------------------------------------------------------------------
PROMPT_TEMPLATE = """\
당신은 주어진 컨텍스트만을 근거로 질문에 답하는 도우미입니다.
컨텍스트에 답이 없으면 "모르겠습니다"라고 말하세요.

[컨텍스트]
{context}

[질문]
{question}

[답변]
"""


def build_prompt(question: str, retrieved: list[tuple[float, Chunk]]) -> str:
    context = "\n".join(
        f"- (doc {c.doc_id}, score={score:.3f}) {c.text}"
        for score, c in retrieved
    )
    return PROMPT_TEMPLATE.format(context=context, question=question)


# ---------------------------------------------------------------------------
# 9) 생성 (Generation)
#    - 실제로는 OpenAI/Anthropic/로컬 LLM API를 호출한다.
#    - 데모에서는 검색된 최상위 청크를 그대로 요약-반환하는 모의 LLM을 사용.
# ---------------------------------------------------------------------------
def mock_llm(prompt: str, retrieved: list[tuple[float, Chunk]]) -> str:
    if not retrieved or retrieved[0][0] == 0.0:
        return "모르겠습니다. (관련 문서를 찾지 못했습니다.)"
    best_score, best_chunk = retrieved[0]
    return (f"[모의 LLM 응답] 가장 관련성 높은 근거(score={best_score:.3f}):\n"
            f"  → {best_chunk.text}")


# ---------------------------------------------------------------------------
# 10) 전체 파이프라인 (RAG Orchestrator)
# ---------------------------------------------------------------------------
class RAGPipeline:
    def __init__(self, chunk_size: int = 60, overlap: int = 10,
                 top_k: int = 3) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.top_k = top_k
        self.store: VectorStore | None = None

    def index(self, documents: list[str]) -> None:
        chunks = split_into_chunks(documents, self.chunk_size, self.overlap)
        self.store = build_vector_store(chunks)

    def ask(self, question: str) -> str:
        if self.store is None:
            raise RuntimeError("먼저 index()를 호출하여 문서를 인덱싱하세요.")
        retrieved = retrieve(self.store, question, top_k=self.top_k)
        prompt = build_prompt(question, retrieved)
        answer = mock_llm(prompt, retrieved)

        # 디버깅용 출력
        print("=" * 60)
        print(f"[질문] {question}")
        print("-" * 60)
        print("[검색 결과 Top-K]")
        for score, chunk in retrieved:
            print(f"  · score={score:.3f} | doc{chunk.doc_id}-c{chunk.chunk_id} "
                  f"| {chunk.text[:40]}...")
        print("-" * 60)
        print("[증강된 프롬프트]")
        print(prompt)
        print("-" * 60)
        print(f"[최종 답변]\n{answer}")
        print("=" * 60)
        return answer


# ---------------------------------------------------------------------------
# 데모 실행
# ---------------------------------------------------------------------------
def main() -> None:
    rag = RAGPipeline(chunk_size=60, overlap=10, top_k=3)

    # [인덱싱 단계] 1~4
    documents = load_documents()
    rag.index(documents)

    # [질의 단계] 5~10
    questions = [
        "RAG가 무엇인가요?",
        "벡터 데이터베이스에는 어떤 것들이 있나요?",
        "파이썬은 누가 만들었나요?",
    ]
    for q in questions:
        rag.ask(q)


if __name__ == "__main__":
    main()
