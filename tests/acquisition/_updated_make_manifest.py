
def make_manifest(
    *,
    destination: Path,
    urls: list[str],
    expected_filename: str | None = None,
    checksum: str | None = None,
    overwrite_existing: bool = False,
) -> AcquisitionManifest:
    """
    Create a deterministic AcquisitionManifest for tests.

    CorpusSource remains responsible for source identity.
    AcquisitionManifest remains responsible for acquisition policy.
    """

    source = CorpusSource(
        source_id="test-source",
        name="Test Source",
        source_type=SourceType.CORPUS,
        source_format=SourceFormat.TEXT,
    )

    return AcquisitionManifest(
        source=source,
        urls=urls,
        destination=destination,
        expected_filename=expected_filename,
        checksum=checksum,
        overwrite_existing=overwrite_existing,
    )
