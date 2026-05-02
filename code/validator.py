import re
from typing import Dict, List, Tuple

# ============================================
# Validation Rules
# ============================================

VALID_STATUS = {"replied", "escalated"}
VALID_REQUEST_TYPES = {"product_issue", "feature_request", "bug", "invalid"}
VALID_PRODUCT_AREAS = {"payments", "billing", "access", "login", "hiring", "submission", "account"}

VAGUE_PATTERNS = [
    r"\bit\s+seems\b",
    r"\blikely\b",
    r"\bmay\s+be\b",
    r"\bcould\s+be\b",
    r"\bmight\s+be\b",
    r"\bprobably\b",
]

FORBIDDEN_CONTACT_PATTERNS = [
    r"\+?\d[\d\-\s]{7,}",  # phone numbers
    r"\b\w+@\w+\.\w+\b",   # emails
    r"https?://\S+",       # URLs
]

FORBIDDEN_KEYWORDS = ["Interpayment", "Ltd", "Inc", "Global Customer Assistance Service"]

# ============================================
# Validation Functions
# ============================================

def validate_status(status: str) -> Tuple[bool, str]:
    """Check if status is valid."""
    if status not in VALID_STATUS:
        return False, f"Invalid status '{status}'. Must be one of {VALID_STATUS}"
    return True, ""


def validate_request_type(request_type: str) -> Tuple[bool, str]:
    """Check if request_type is valid."""
    if request_type not in VALID_REQUEST_TYPES:
        return False, f"Invalid request_type '{request_type}'. Must be one of {VALID_REQUEST_TYPES}"
    return True, ""


def validate_product_area(product_area: str) -> Tuple[bool, str]:
    """Check if product_area is valid."""
    if product_area not in VALID_PRODUCT_AREAS:
        return False, f"Invalid product_area '{product_area}'. Must be one of {VALID_PRODUCT_AREAS}"
    return True, ""


def validate_response_safety(response: str) -> Tuple[bool, List[str]]:
    """Check for unsafe content in response."""
    issues = []

    # Check for contact details
    for pattern in FORBIDDEN_CONTACT_PATTERNS:
        if re.search(pattern, response):
            issues.append(f"Found forbidden contact pattern: {pattern}")

    # Check for forbidden keywords
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in response:
            issues.append(f"Found forbidden keyword: {keyword}")

    # Check for vague language
    for pattern in VAGUE_PATTERNS:
        if re.search(pattern, response, re.IGNORECASE):
            issues.append(f"Found vague phrasing: {pattern}")

    return len(issues) == 0, issues


def validate_response_length(response: str) -> Tuple[bool, str]:
    """Check if response is reasonable length (not empty, not too long)."""
    if not response or len(response.strip()) == 0:
        return False, "Response is empty"
    if len(response.split()) > 200:
        return False, f"Response is too long ({len(response.split())} words, max 200)"
    return True, ""


def validate_justification(justification: str) -> Tuple[bool, str]:
    """Check if justification is present and reasonable."""
    if not justification or len(justification.strip()) == 0:
        return False, "Justification is empty"
    if len(justification) > 500:
        return False, "Justification is too long"
    return True, ""


# ============================================
# Full Row Validation
# ============================================

def validate_row(result: Dict, row_number: int = None) -> Tuple[bool, List[str]]:
    """Validate a single result row and return (is_valid, list_of_errors)."""
    errors = []
    row_prefix = f"[Row {row_number}]" if row_number else ""

    # Validate status
    is_valid, msg = validate_status(result.get("status", ""))
    if not is_valid:
        errors.append(f"{row_prefix} {msg}")

    # Validate request_type
    is_valid, msg = validate_request_type(result.get("request_type", ""))
    if not is_valid:
        errors.append(f"{row_prefix} {msg}")

    # Validate product_area
    is_valid, msg = validate_product_area(result.get("product_area", ""))
    if not is_valid:
        errors.append(f"{row_prefix} {msg}")

    # Validate response safety
    response = result.get("response", "")
    is_safe, safety_issues = validate_response_safety(response)
    if not is_safe:
        for issue in safety_issues:
            errors.append(f"{row_prefix} Response: {issue}")

    # Validate response length
    is_valid, msg = validate_response_length(response)
    if not is_valid:
        errors.append(f"{row_prefix} Response: {msg}")

    # Validate justification
    is_valid, msg = validate_justification(result.get("justification", ""))
    if not is_valid:
        errors.append(f"{row_prefix} Justification: {msg}")

    return len(errors) == 0, errors


def validate_batch(results: List[Dict]) -> Tuple[bool, List[str], Dict]:
    """Validate a batch of results and return stats."""
    errors = []
    stats = {
        "total": len(results),
        "valid": 0,
        "invalid": 0,
        "replied": 0,
        "escalated": 0,
        "by_status": {},
        "by_request_type": {},
        "by_product_area": {},
    }

    for i, result in enumerate(results, 1):
        is_valid, row_errors = validate_row(result, i)

        if is_valid:
            stats["valid"] += 1
        else:
            stats["invalid"] += 1
            errors.extend(row_errors)

        # Count stats
        status = result.get("status", "unknown")
        stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
        if status == "replied":
            stats["replied"] += 1
        elif status == "escalated":
            stats["escalated"] += 1

        request_type = result.get("request_type", "unknown")
        stats["by_request_type"][request_type] = stats["by_request_type"].get(request_type, 0) + 1

        product_area = result.get("product_area", "unknown")
        stats["by_product_area"][product_area] = stats["by_product_area"].get(product_area, 0) + 1

    return len(errors) == 0, errors, stats


def print_validation_report(results: List[Dict], title: str = "Validation Report"):
    """Print a formatted validation report."""
    is_valid, errors, stats = validate_batch(results)

    print(f"\n{'='*80}")
    print(f"{title}")
    print(f"{'='*80}")

    print(f"\n📊 Summary:")
    print(f"  Total rows: {stats['total']}")
    print(f"  ✅ Valid: {stats['valid']}")
    print(f"  ❌ Invalid: {stats['invalid']}")
    print(f"  Valid rate: {100 * stats['valid'] / stats['total']:.1f}%")

    print(f"\n📋 Status Distribution:")
    print(f"  Replied: {stats['replied']} ({100 * stats['replied'] / stats['total']:.1f}%)")
    print(f"  Escalated: {stats['escalated']} ({100 * stats['escalated'] / stats['total']:.1f}%)")

    print(f"\n📦 Request Type Distribution:")
    for rt, count in sorted(stats["by_request_type"].items()):
        print(f"  {rt}: {count}")

    print(f"\n🏷️  Product Area Distribution:")
    for pa, count in sorted(stats["by_product_area"].items()):
        print(f"  {pa}: {count}")

    if errors:
        print(f"\n⚠️  Validation Errors ({len(errors)}):")
        for error in errors[:50]:
            print(f"  - {error}")
        if len(errors) > 50:
            print(f"  ... and {len(errors) - 50} more errors")

    print(f"\n{'='*80}\n")

    return is_valid
