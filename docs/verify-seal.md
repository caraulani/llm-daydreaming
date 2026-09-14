# Verifying the preregistration seal

Three independent timestamps say the protocol preceded the data.

## 1. Git ancestry

```bash
git rev-list -n1 v0.1.0-prereg                    # the seal commit
git log --reverse --format=%H -- 'experiments/runs/public/*_micro/**' | head -n1   # first results commit
git merge-base --is-ancestor $(git rev-list -n1 v0.1.0-prereg) <first results commit> && echo OK
```

`.github/workflows/prereg-ancestry.yml` runs this on every push. The same applies to `v0.2.0-prereg` and `experiments/runs/public/*_micro_v0_2/**`.

## 2. OpenTimestamps (Bitcoin)

The `.ots` proofs cover the sealed versions of the files, which are the blobs at the seal tags. The working-tree `PREREGISTRATION.md` has changed since the seal (post-seal fields and the DEVIATIONS section, as the file itself allows), so verify against the sealed blob:

```bash
git show v0.1.0-prereg:PREREGISTRATION.md > /tmp/prereg_sealed.md
ots verify -f /tmp/prereg_sealed.md PREREGISTRATION.md.ots
ots verify data/synth/v0.1/bridges.yaml.ots        # answer key, unchanged since the seal
ots verify data/synth/v0.1/decoys.yaml.ots
```

`ots verify` needs a local Bitcoin node to check the block header. Without one, `ots info PREREGISTRATION.md.ots` prints the attestation, including the Bitcoin block height and the merkle root the proof commits to; compare the merkle root with any block explorer's record of that block. The v0.1 proofs were upgraded on 2026-09-14 and attest in block 966837. The v0.2 proofs (`PREREGISTRATION-v0.2.md.ots`, `data/synth/v0.2/*.ots`) were stamped on 2026-09-13 and upgraded on 2026-09-14; they attest in block 966878. The v0.3 proofs (`PREREGISTRATION-v0.3.md.ots`, `data/synth/v0.3/*.ots`, `prompts/generate_single_strict.md.ots`) attest in block 966979. To upgrade a pending proof yourself:

```bash
ots upgrade PREREGISTRATION-v0.2.md.ots
```

## 3. Commit signatures

Every commit is signed with the author's SSH key. On GitHub, signed commits show a Verified badge once the key is registered as a signing key; locally:

```bash
git log --show-signature -1 v0.1.0-prereg
```

Local verification needs `gpg.ssh.allowedSignersFile` configured with the author's public key.
