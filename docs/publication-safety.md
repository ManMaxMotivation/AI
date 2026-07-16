# Publication Safety Checklist

Use this checklist before adding any example, screenshot, log, test case, or
agent rule derived from private work.

## Required Review

1. Rebuild the example from a general behavior. Do not edit and publish an
   existing private artifact.
2. Remove credentials, keys, cookies, phone numbers, email addresses, OTPs,
   customer data, test accounts, and personal names.
3. Remove internal domains, URLs, IP addresses, cloud IDs, service names,
   issue IDs, merge-request IDs, environment labels, local paths, and project
   code names.
4. Remove proprietary code, schema fragments, logs, screenshots, attachments,
   and architecture information that identifies the source system.
5. Replace all values with fictional names and values. Confirm that the flow
   still explains a general QA risk without revealing the original system.
6. Review the staged diff line by line and run the secret scan before push.

## What a Scanner Cannot Decide

Automated scanners can detect many credential patterns. They cannot reliably
detect business-sensitive terms, an identifiable architecture, customer
context, or a screenshot that exposes an internal product. Human review is
mandatory for every public contribution derived from work.

## Repository Guardrail

The repository runs a secret scan for pushes and pull requests. A passing scan
is necessary but never sufficient for publication.
