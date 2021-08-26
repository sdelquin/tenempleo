import re


def is_target_job(job_text: str, targets: list[str]):
    for term in targets:
        if all([re.search(rf'\b{w}\b', job_text, re.I) for w in re.split(r'[ ,]+', term)]):
            return True
    return False
