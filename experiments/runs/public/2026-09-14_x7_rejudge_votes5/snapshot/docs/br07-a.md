## VAT transition fallout

Switched legal form on 1 April. Old VAT number ending 771 is on all invoices before that date; new number ending 402 from April onwards. Creating friction points with payment reconciliation and some backend integrations that cache the old identifier. Need to audit which systems still reference the old number.

## 2025 accounts filing

Submitted annual accounts under the old VAT registration since the period spanned both forms. Now reconciling invoice records for next year's tax prep: pre-April invoices carry the old identifier, post-April ones the new. Some accounting software isn't handling the dual numbering cleanly in reconciliation reports.

## Invoice cleanup

Most payment processors accepted the April transition without issue, but manual invoices issued in early April are scattered between the two numbers. Drafting a checklist for next filing cycle to ensure consistency. Also flagging that any third-party systems pulling invoice metadata will need to know both identifiers exist in the record.