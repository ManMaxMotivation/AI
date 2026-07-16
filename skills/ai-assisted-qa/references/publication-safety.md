# Publication Safety

Treat every task artifact as private by default. Publish only a synthetic
reconstruction of a general pattern, never a lightly edited copy of work.

Before publication, remove or replace:

- credentials, tokens, cookies, keys, phone numbers, email addresses, and OTPs;
- private hostnames, URLs, IP addresses, service names, environment names, and
  cloud identifiers;
- issue, merge-request, customer, order, inventory, or employee identifiers;
- proprietary source fragments, database schemas, logs, screenshots, and
  internal architecture details;
- test accounts, sample records, attachments, and artifacts that can reveal a
  real system through metadata or visual content.

Keep only the generalized behavior, risk, test logic, and evidence shape. Use
fictional names and values. Verify that a reader cannot reconstruct the real
company, system, customer, or access route from the example.

Run the repository secret scan and review all added files before pushing. A scan
cannot reliably detect business-sensitive details, so a human privacy review is
mandatory.
