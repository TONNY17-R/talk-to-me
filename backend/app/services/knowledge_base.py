"""Knowledge base for the Talk to Me AI assistant.

This module contains curated informational content about the platform, its
features, and how to get help. The AI service uses this to provide accurate
responses to user questions without needing to call an external LLM.
"""

from typing import Dict, List, Optional


KNOWLEDGE_ENTRIES = [
    {
        "keywords": [
            "talk to me",
            "what is talk to me",
            "what do you do",
            "what is this",
            "what is this app",
            "what is this platform",
        ],
        "response": {
            "en": (
                "Talk to Me is a mental health support platform built for Uganda. "
                "It provides an AI chat assistant, mental health assessments, "
                "access to professional counselling, and a library of resources "
                "to help you manage your wellbeing."
            ),
            "lg": (
                "Talk to Me ye platform ey'obulamu obulungi mu Uganda. "
                "Ekyusa omuntu mu ngeri y'okukwata mu kusanyusa embeera y'omubiri, "
                "ekitwala obuwanguzi n'okunyweza okw'obulamu obulungi."
            ),
            "sw": (
                "Talk to Me ni jukwaa la msaada wa afya ya akili kwa Uganda. "
                "Inatoa gumzo la AI, tathmini za afya ya akili, msaada wa wataalamu, "
                "na rasilimali za kujisaidia mwenyewe."
            ),
        },
    },
    {
        "keywords": [
            "assessments",
            "phq",
            "gad",
            "mental health assessment",
            "quiz",
        ],
        "response": {
            "en": (
                "You can take the PHQ-9 and GAD-7 assessments to evaluate your "
                "mood, anxiety, and stress levels. These are common screening tools "
                "used by healthcare professionals to help understand how you are feeling."
            ),
            "lg": (
                "Osobola okukola PHQ-9 ne GAD-7 okw'enjigiriza engeri gy'oyitamu ebintu nga okusiiga mu mutima, "
                "okunstuula, n'okuweddeka. Buli omu kuziikozi guno gukoze nga balina okukusobozesa "
                "okugenda mu maaso."
            ),
            "sw": (
                "Unaweza kufanya tathmini za PHQ-9 na GAD-7 kuangalia hisia zako, wasiwasi, na msongo. "
                "Hizi ni zana za kawaida zinazotumika na wataalamu wa afya ya akili."
            ),
        },
    },
    {
        "keywords": [
            "counselling",
            "counselor",
            "counsellor",
            "professional help",
            "therapy",
        ],
        "response": {
            "en": (
                "Professional counselling connects you with trained mental health "
                "counsellors who can listen, offer strategies, and support you through "
                "difficult moments. You can book a session through the counselling section."
            ),
            "lg": (
                "Okuyambibwa ng'omuntu alya omulimu kukwe nga'ba counselor baali bamanyi nnyo. "
                "Bamaliriza okukuwonya era bakuyamba okwetegereza by'oba okusobola okukozesa. "
                "Osobola okukyusa ekiseera mu kibiina kyokuyambibwa."
            ),
            "sw": (
                "Ushauri wa kitaalamu unakuunganisha na washauri waliofunzwa ambao wanaweza kusikia, "
                "kukupa mikakati, na kukuunga mkono wakati wa wakati mgumu. Unaweza kuomba kikao kupitia sehemu ya ushauri."
            ),
        },
    },
    {
        "keywords": [
            "crisis",
            "suicide",
            "self harm",
            "hurt myself",
            "kill myself",
            "end my life",
        ],
        "response": {
            "en": (
                "If you are in immediate danger or considering harming yourself, please "
                "reach out to local emergency services right away. You can also contact "
                "a crisis hotline, talk to someone you trust, or use the in-app crisis support options." 
            ),
            "lg": (
                "Bw'oba ofunye obuzibu obw'akabi oba okwegombaaga okusaasira, wandiikira abantu abali mu nsi yonna "
                "ab'ekibiina ky'eby'obulamu obw'omubiri. Osobola n'okwebuuza ku kisumuluzo ky'obuzibu oba "
                "okugamba omuntu ow'owulira."
            ),
            "sw": (
                "Kama uko katika hatari ya haraka au unafikiria kujidhalilisha, tafadhali wasiliana na huduma za dharura za eneo lako mara moja. "
                "Unaweza pia kupiga simu ya msaada wa dharura, kuzungumza na mtu unaemwamini, au kutumia chaguzi za msaada wa dharura ndani ya app." 
            ),
        },
    },
]


def get_knowledge_response(query: str, language: str = 'en') -> Optional[str]:
    """Return a knowledge-based response if the query matches known topics."""
    if not query:
        return None

    query_lower = query.lower()

    for entry in KNOWLEDGE_ENTRIES:
        for keyword in entry["keywords"]:
            if keyword in query_lower:
                return entry["response"].get(language, entry["response"].get('en'))

    return None
