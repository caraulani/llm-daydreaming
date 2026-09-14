---
name: dc07-b
---
```yaml
---
name: Merchant descriptor update for calling app
description: Changing card statement text to show brand name instead of generic processor name
type: project
---
```

# Merchant descriptor on card statements

Cardholder complaints came in: they see "PAYMENT PROCESSOR INC" on their statements instead of the actual brand. Charge back inquiries up 12% this quarter, mostly "did not recognize charge" disputes. Descriptor text determines what shows in the 22-character field on card statements.

## Current state

Processor's dashboard allows updating the descriptor through their merchant portal. Currently shows the old processor name from initial account setup. Need to change to brand name so people recognize their own charges. Max 22 chars for descriptor, 10 additional for transaction details, total 32.

## Action items

- Access merchant portal with account manager login
- Update descriptor field to brand name (17 chars, fits)
- Test with test card through staging environment, verify statement text
- Add to FAQ/onboarding since first-time users may not recognise the charge anyway
- Monitor next dispute batch for descriptor-related claims

## Timeline

Customers reporting since late August. Push to live by end of week. Processor takes 1-2 business days to sync after portal update.

```
