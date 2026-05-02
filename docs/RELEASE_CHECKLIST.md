# Release Checklist for Vibe-Linux

Use this checklist when preparing a new release.

## Pre-Release (1 week before)

### Code Quality
- [ ] Run `bash scripts/smoke-test.sh` - all tests pass
- [ ] Run `python -m compileall tools installer examples/plugins`
- [ ] Check for any compiler warnings
- [ ] Review recent commits for quality
- [ ] No debug code or commented-out sections

### Testing
- [ ] Test installation on x86_64
- [ ] Test installation on aarch64
- [ ] Test all UI presets (default, Windows 11, macOS)
- [ ] Test all performance modes (full, lite, performance)
- [ ] Test WiFi and network
- [ ] Test GPU driver detection
- [ ] Test vibectl commands
- [ ] Test plugin system

### Documentation
- [ ] Update RELEASE_NOTES.md
- [ ] Update docs/ with any new features
- [ ] Update README.md if needed
- [ ] Update INSTALLATION.md if needed
- [ ] Review CONTRIBUTING.md for completeness
- [ ] Check for broken links in documentation

### Security
- [ ] Run `trivy fs .`
- [ ] Check for secret leaks
- [ ] Review security.md for relevance
- [ ] Ensure all dependencies are up-to-date

## Release Day

### Preparation
- [ ] Ensure all commits are pushed
- [ ] All CI/CD tests passing
- [ ] No open blocker issues
- [ ] Team approval for release

### Build
- [ ] Create annotated git tag: `git tag -a v0.2.0 -m "Release notes"`
- [ ] Push tag: `git push origin v0.2.0`
- [ ] Wait for GitHub Actions to complete
- [ ] Verify ISOs in releases
- [ ] Verify SHA256 checksums
- [ ] Test download links

### Release Notes
- [ ] Create GitHub Release
- [ ] Include generated release notes from GitHub Actions
- [ ] Add contributor list
- [ ] Add thank you message
- [ ] Link to detailed changelog

### Announcement
- [ ] Announce on GitHub Discussions
- [ ] Update website (if applicable)
- [ ] Social media announcement (if applicable)
- [ ] Ask for feedback

## Post-Release (1-2 days after)

### Monitoring
- [ ] Monitor GitHub issues for bugs
- [ ] Check for installation failures
- [ ] Respond to user feedback
- [ ] Identify hotfix candidates

### Follow-up
- [ ] Create issues for reported problems
- [ ] Plan hotfix release if critical issues found
- [ ] Update project status
- [ ] Plan next release

## Hotfix Release (if needed)

### For critical bugs only
- [ ] Fix the bug
- [ ] Run full test suite
- [ ] Create v0.2.1 tag
- [ ] Follow normal release process
- [ ] Note hotfix in release description

## Release Versioning

Follow [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH`
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

## Example Release Command Sequence

```bash
# Prepare release
git pull origin main
bash scripts/smoke-test.sh
python -m compileall tools installer examples/plugins

# Create tag and push
git tag -a v0.2.0 -m "Release v0.2.0: Production-ready with macOS preset"
git push origin v0.2.0

# Wait for GitHub Actions...

# Create GitHub Release with notes
# Download ISOs and verify checksums
# Announce to community
```

## Success Criteria

- ✅ All tests pass
- ✅ No critical issues reported
- ✅ Documentation is up-to-date
- ✅ ISOs are available for download
- ✅ Installation works on tested hardware
- ✅ Community feedback is positive

---

For questions, contact the team on GitHub Discussions.
