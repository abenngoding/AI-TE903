from dataclasses import dataclass
from typing import List


@dataclass
class AgentResult:
    agent: str
    content: str


class ResearchAgent:
    name = "ResearchAgent"

    def run(self, topic: str) -> AgentResult:
        # Contoh sederhana berbasis aturan, bukan pencarian internet sungguhan.
        points = [
            f"Topik utama yang dibahas adalah: {topic}.",
            "Tentukan tujuan dan ruang lingkup masalah.",
            "Kumpulkan fakta atau data yang relevan sebelum mengambil keputusan.",
        ]
        return AgentResult(self.name, "\n".join(f"- {p}" for p in points))


class AnalysisAgent:
    name = "AnalysisAgent"

    def run(self, topic: str, research: str) -> AgentResult:
        analysis = (
            f"Analisis untuk '{topic}':\n"
            "- Identifikasi kebutuhan dan batasan sistem.\n"
            "- Bandingkan beberapa alternatif solusi.\n"
            "- Periksa risiko, biaya, dan manfaat sebelum memilih solusi.\n"
            f"\nBahan dari ResearchAgent:\n{research}"
        )
        return AgentResult(self.name, analysis)


class SummaryAgent:
    name = "SummaryAgent"

    def run(self, topic: str, analysis: str) -> AgentResult:
        summary = (
            f"Ringkasan: Untuk topik '{topic}', mulai dengan menetapkan tujuan, "
            "mengumpulkan data, lalu mengevaluasi alternatif berdasarkan kebutuhan "
            "dan risiko. Hasil ini adalah demo sederhana dan perlu diverifikasi "
            "dengan data nyata.\n"
            "\nRekomendasi langkah berikutnya:\n"
            "1. Tentukan masalah secara spesifik.\n"
            "2. Masukkan data nyata yang relevan.\n"
            "3. Evaluasi hasil dan validasi kesimpulan."
        )
        return AgentResult(self.name, summary)


class MultiAgentSystem:
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.analysis_agent = AnalysisAgent()
        self.summary_agent = SummaryAgent()

    def run(self, topic: str) -> List[AgentResult]:
        research = self.research_agent.run(topic)
        analysis = self.analysis_agent.run(topic, research.content)
        summary = self.summary_agent.run(topic, analysis.content)
        return [research, analysis, summary]


def main():
    print("=" * 60)
    print("DEMO MULTI-AGENT SYSTEM")
    print("=" * 60)
    topic = input("Masukkan topik atau masalah: ").strip()
    if not topic:
        topic = "Otomasi industri berbasis AI"

    system = MultiAgentSystem()
    results = system.run(topic)

    for result in results:
        print(f"\n[{result.agent}]")
        print("-" * 60)
        print(result.content)

    print("\nDemo selesai. Agen-agen ini menggunakan aturan contoh lokal,")
    print("bukan model AI eksternal atau pencarian internet.")


if __name__ == "__main__":
    main()
