"""Manually curated, non-production content for the AL Sydbank MVP pilot."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PilotItem:
    title: str
    detail: str
    information_type: str
    source_label: str
    period: str


@dataclass(frozen=True)
class CommercialHypothesis:
    title: str
    evidence: str
    observation: str
    potential_need: str
    thursday_relevance: str
    source_label: str
    period: str


PILOT_ENTITY = "AL Sydbank"
H1_2026_SOURCE = "AL Sydbank H1 2026 interim-report material"
THURSDAY_SEPTEMBER_2026_SOURCE = "Thursday material for AL Sydbank benchmarking Danske Bank"

MERGER_FACTS = (
    PilotItem(
        "Integration costs",
        "H1 2026 integration costs related to the merger were reported as DKK 32m.",
        "Fact",
        H1_2026_SOURCE,
        "H1 2026",
    ),
    PilotItem(
        "BEC exit compensation",
        "The reported integration costs primarily relate to BEC exit compensation.",
        "Fact",
        H1_2026_SOURCE,
        "H1 2026",
    ),
    PilotItem(
        "Liquidity effect",
        "The merger was reported to have a positive liquidity effect of DKK 12,485m.",
        "Fact",
        H1_2026_SOURCE,
        "H1 2026",
    ),
    PilotItem(
        "Acquisition goodwill",
        "Goodwill related to the acquisition was reported as DKK 7,689m.",
        "Fact",
        H1_2026_SOURCE,
        "H1 2026",
    ),
    PilotItem(
        "Reported synergy context",
        "The report states that goodwill can partly be related to significant cost and capital synergies.",
        "Fact",
        H1_2026_SOURCE,
        "H1 2026",
    ),
)

THURSDAY_PERSPECTIVES = (
    PilotItem(
        "Benchmarking coverage",
        "Thursday has developed client-specific material covering scale and footprint, customer and service model, AI and technology, and IT / operating-model considerations.",
        "Thursday perspective",
        THURSDAY_SEPTEMBER_2026_SOURCE,
        "September 2026",
    ),
    PilotItem(
        "Benchmarking perspective",
        "Thursday's material argues for benchmarking capabilities rather than copying Danske Bank's model.",
        "Thursday perspective",
        THURSDAY_SEPTEMBER_2026_SOURCE,
        "September 2026",
    ),
    PilotItem(
        "Relevant lenses",
        "Thursday highlights simplicity, relationships, and selective technology as relevant perspectives for the benchmark discussion.",
        "Thursday perspective",
        THURSDAY_SEPTEMBER_2026_SOURCE,
        "September 2026",
    ),
)

PERFORMANCE_GUIDANCE = PilotItem(
    "Existing Databank capability",
    "Use Bank → Bank Analyst View for AL Sydbank financial performance and peer benchmarking; this MVP does not create a parallel analytics engine.",
    "MVP guidance",
    "Existing Databank Bank Analyst View",
    "Current application",
)

COMMERCIAL_HYPOTHESES = (
    CommercialHypothesis(
        "Merger integration and synergy realisation",
        "Reported H1 2026 merger integration costs, BEC exit compensation, liquidity effect, acquisition goodwill, and synergy context.",
        "Thursday's existing material includes IT and operating-model considerations.",
        "Potential need to structure discussion of integration progress and the realisation of cost and capital synergies.",
        "Thursday could bring a capability-benchmarking lens to the discussion.",
        f"{H1_2026_SOURCE}; {THURSDAY_SEPTEMBER_2026_SOURCE}",
        "H1 2026 / September 2026",
    ),
    CommercialHypothesis(
        "Customer and service model",
        "No AL Sydbank customer-model fact is connected in this MVP.",
        "Thursday's client-specific material covers customer and service model and emphasises relationships as a perspective.",
        "Potential need to explore how customer and service capabilities should be benchmarked during integration.",
        "Thursday could frame a comparison around capabilities rather than copying Danske Bank's model.",
        THURSDAY_SEPTEMBER_2026_SOURCE,
        "September 2026",
    ),
    CommercialHypothesis(
        "Selective AI and technology",
        "No AL Sydbank AI or technology fact is connected in this MVP.",
        "Thursday's client-specific material covers AI and technology and highlights selective technology as a perspective.",
        "Potential need to identify where selective technology capabilities warrant a focused benchmark discussion.",
        "Thursday could support a capability-based benchmark without implying a confirmed client requirement.",
        THURSDAY_SEPTEMBER_2026_SOURCE,
        "September 2026",
    ),
)
