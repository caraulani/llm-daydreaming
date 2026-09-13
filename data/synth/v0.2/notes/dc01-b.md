---
name: Failed Login Spike Post-Reset
description: Unexpected spike in failed login attempts during 48-hour window following forced password reset notification
type: project
---

# Failed Login Spike Post-Reset

## Timeline

- Sept 10: sent forced password-reset email to all active users due to security review
- Sept 11-12: 340% increase in failed login attempts vs. daily average
- Peak at Sept 11 evening, declined Sept 12 afternoon
- Returned to baseline by Sept 13 morning

## Possible factors

- Users not checking email immediately, attempting login with old credentials
- Email delivery delays causing 12-24hr gap between reset and account access
- Mobile app caching old tokens, retry loops on auth failure
- Phishing emails impersonating reset, check logs for reply-to pattern

## What we measured

- Failed attempts: 2,847 across both platforms (app + web)
- No successful breaches during spike window
- Unique IP addresses: mostly known user locations
- No correlation with account signup date or geography

## Next steps

- Pull email delivery logs, cross-check with failed login timestamps
- Test app token cache on fresh install
- Review support ticket volume Sept 11-12 for user confusion reports
- Consider staggered reset windows for future campaigns
