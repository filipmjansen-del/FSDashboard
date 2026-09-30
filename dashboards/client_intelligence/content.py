"""Manually curated, non-production content for the AL Sydbank MVP pilot."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceMetadata:
    publisher: str
    title: str
    publication_date: str
    source_type: str
    page_reference: str | None = None
    url: str | None = None


@dataclass(frozen=True)
class PilotItem:
    title: str
    detail: str
    information_type: str
    source: SourceMetadata
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
    source_urls: tuple[str, ...]


PILOT_ENTITY = "AL Sydbank"
H1_2026_SOURCE_TITLE = "Delårsrapport - 1. halvår 2026"
H1_2026_SOURCE_URL = "https://ml-eu.globenewswire.com/Resource/Download/c2791f30-e63c-466a-93a8-ec58739d267e"
H1_2026_PAGE_30_SOURCE = SourceMetadata(
    publisher="AL Sydbank A/S",
    title=H1_2026_SOURCE_TITLE,
    publication_date="26 August 2026",
    source_type="Official company reporting",
    page_reference="Page 30",
    url=H1_2026_SOURCE_URL,
)
H1_2026_PAGE_46_SOURCE = SourceMetadata(
    publisher="AL Sydbank A/S",
    title=H1_2026_SOURCE_TITLE,
    publication_date="26 August 2026",
    source_type="Official company reporting",
    page_reference="Page 46",
    url=H1_2026_SOURCE_URL,
)
THURSDAY_SEPTEMBER_2026_SOURCE = SourceMetadata(
    publisher="Thursday",
    title="Thursday material for AL Sydbank benchmarking Danske Bank",
    publication_date="September 2026",
    source_type="Thursday material",
)
CUSTOMER_PROPOSITION_SOURCE = SourceMetadata(
    publisher="AL Sydbank A/S", title="Farvel til gebyr", publication_date="September 2026",
    source_type="Official company news", url="https://www.al-sydbank.dk/nyt/farvel-til-gebyr",
)
MERGER_POSITIONING_SOURCE = SourceMetadata(
    publisher="AL Sydbank A/S", title="Fusionen til AL Sydbank er nu en realitet", publication_date="2026",
    source_type="Official company news", url="https://www.al-sydbank.dk/nyt/fusionen-til-al-sydbank-er-nu-en-realitet",
)
LARGER_BANK_SOURCE = SourceMetadata(
    publisher="AL Sydbank A/S", title="Vi vil skabe en større bank", publication_date="2026",
    source_type="Official company news", url="https://www.al-sydbank.dk/nyt/vi-vil-skabe-en-stoerre-bank",
)
ORGANISATION_SOURCE = SourceMetadata(
    publisher="AL Sydbank A/S", title="Organisation", publication_date="Current public organisation page",
    source_type="Official company information", url="https://www.al-sydbank.dk/om-os/organisation",
)

MERGER_FACTS = (
    PilotItem(
        "Integration costs",
        "H1 2026 integration costs related to the merger were reported as DKK 32m.",
        "Fact",
        H1_2026_PAGE_30_SOURCE,
        "H1 2026",
    ),
    PilotItem(
        "BEC exit compensation",
        "The reported integration costs primarily relate to BEC exit compensation.",
        "Fact",
        H1_2026_PAGE_30_SOURCE,
        "H1 2026",
    ),
    PilotItem(
        "Liquidity effect",
        "The merger was reported to have a positive liquidity effect of DKK 12,485m.",
        "Fact",
        H1_2026_PAGE_46_SOURCE,
        "H1 2026",
    ),
    PilotItem(
        "Acquisition goodwill",
        "Goodwill related to the acquisition was reported as DKK 7,689m.",
        "Fact",
        H1_2026_PAGE_46_SOURCE,
        "H1 2026",
    ),
    PilotItem(
        "Reported synergy context",
        "The report states that goodwill can partly be related to significant cost and capital synergies.",
        "Fact",
        H1_2026_PAGE_46_SOURCE,
        "H1 2026",
    ),
)

THURSDAY_PERSPECTIVES = (
    PilotItem(
        "Benchmarking coverage",
        "Thursday has developed client-specific benchmarking material covering customer and service model, technology, and platform / operating-model considerations.",
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

CUSTOMER_PROPOSITION_SIGNAL = PilotItem(
    "Customer proposition", "AL Sydbank removed account and netbank fees for relevant private customers.",
    "Fact", CUSTOMER_PROPOSITION_SOURCE, "September 2026",
)
STRATEGIC_POSITIONING_SIGNAL = PilotItem(
    "Strategic positioning", "Public merger communication describes a broader offering, more specialist capabilities, stronger digital solutions, and a national/local distribution footprint.",
    "Fact", MERGER_POSITIONING_SOURCE, "2026",
)
PUBLIC_EXECUTIVES = (
    PilotItem("Mark Luscombe", "CEO", "Fact", ORGANISATION_SOURCE, "Current public organisation page"),
    PilotItem("Frank Mortensen", "Vice CEO", "Fact", ORGANISATION_SOURCE, "Current public organisation page"),
    PilotItem("Jørn Adam Møller", "CFO", "Fact", ORGANISATION_SOURCE, "Current public organisation page"),
    PilotItem("Svend Randers", "Bankdirektør", "Fact", ORGANISATION_SOURCE, "Current public organisation page"),
    PilotItem("Gry Bandholm", "Bankdirektør", "Fact", ORGANISATION_SOURCE, "Current public organisation page"),
)
INTERNAL_ACCOUNT_MAPPING = tuple(
    f"{person.title} — Account mapping available" for person in PUBLIC_EXECUTIVES
)
THURSDAY_CAPABILITIES = (
    "Integration & programme execution", "Customer & service model", "Technology & architecture", "Operating model & governance",
)

PERFORMANCE_GUIDANCE = PilotItem(
    "Existing Databank capability",
    "Use Bank → Bank Analyst View for AL Sydbank financial performance and peer benchmarking; this MVP does not create a parallel analytics engine.",
    "MVP guidance",
    SourceMetadata(
        publisher="Databank",
        title="Bank Analyst View",
        publication_date="Current application",
        source_type="Existing Databank capability",
    ),
    "Current application",
)

COMMERCIAL_HYPOTHESES = (
    CommercialHypothesis(
        "Merger integration and synergy realisation",
        "Reported H1 2026 merger integration costs, BEC exit compensation, liquidity effect, acquisition goodwill, and synergy context.",
        "Thursday's existing material includes IT and operating-model considerations.",
        "Potential need to structure discussion of integration progress and the realisation of cost and capital synergies.",
        "Thursday could bring a capability-benchmarking lens to the discussion.",
        f"{H1_2026_SOURCE_TITLE}; {THURSDAY_SEPTEMBER_2026_SOURCE.title}",
        "H1 2026 / September 2026",
        (H1_2026_SOURCE_URL,),
    ),
    CommercialHypothesis(
        "Customer and service model",
        "Public merger positioning and the September 2026 private-customer fee change.",
        "Thursday's client-specific material covers customer and service model and emphasises relationships as a perspective.",
        "Potential need to structure discussion of future service model, segmentation, and channel or branch choices.",
        "Thursday relevance: Customer & service model.",
        f"{CUSTOMER_PROPOSITION_SOURCE.title}; {MERGER_POSITIONING_SOURCE.title}",
        "2026",
        (CUSTOMER_PROPOSITION_SOURCE.url, MERGER_POSITIONING_SOURCE.url),
    ),
    CommercialHypothesis(
        "Digital & platform enablement",
        "Public ambition for stronger digital solutions.",
        "Thursday's benchmarking material covers technology and platform / operating-model considerations.",
        "Potential need to translate a future service model into platform and technology requirements.",
        "Thursday relevance: Technology & architecture.",
        f"{MERGER_POSITIONING_SOURCE.title}; {LARGER_BANK_SOURCE.title}",
        "2026",
        (MERGER_POSITIONING_SOURCE.url, LARGER_BANK_SOURCE.url),
    ),
)
