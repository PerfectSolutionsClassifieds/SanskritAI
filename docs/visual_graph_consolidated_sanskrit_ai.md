  📂 SanskritAI/
    📄 __init__.py
    📄 main.py
        ⚙️ Functions:
          • build_parser()
          • main()
    📄 run_all_tests.py
        🔹 Constants:
          • TEST_MODULES
    📂 acquisition/
      📄 __init__.py
      📄 acquisition_manager.py
          🏗️ Classes:
            • class AcquisitionManager:
              - __init__(self)
              - register_provider(self, provider)
              - provider(self, identifier)
              - register_repository(self, repository)
              - register_validator(self, validator)
              - set_normalizer(self, normalizer)
              - discover(self, request)
              - acquire(self, request)
              - _validate_downloads(self, files)
              - _normalize_downloads(self, files)
              - repository_health(self)
              - providers(self)
              - repositories(self)
              - validators(self)
              - provider_identifiers(self)
              - clear(self)
              - __len__(self)
              - __contains__(self, provider)
              - __repr__(self)
      📂 acquirers/
        📄 default_source_acquirer.py
            🏗️ Classes:
              • class DefaultSourceAcquirer:
                - acquire(self, manifest)
                - _validate_manifest(self, manifest, result)
                - _prepare_destination(self, manifest)
                - _download_from_sources(self, manifest, destination_directory, result)
                - _download_one(self, url, manifest, destination_directory)
                - _copy_local_file(self, url, destination)
                - _download_http(self, url, destination)
                - _resolve_filename(self, url, manifest)
                - _verify_checksum(self, manifest, path, result)
                - __repr__(self)
                - __str__(self)
        📄 source_acquirer.py
            🏗️ Classes:
              • class SourceAcquirer:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - acquire(self, manifest)
                - __str__(self)
      📂 detectors/
        📄 __init__.py
        📄 source_format_detector.py
            🏗️ Classes:
              • class SourceFormatDetector:
                - detect(cls, path)
                - is_supported(cls, path)
                - supported_extensions(cls)
                - register_extension(cls, extension, source_format)
                - unregister_extension(cls, extension)
                - __repr__(self)
      📂 discovery/
        📄 __init__.py
        📄 base_discovery_provider.py
            🏗️ Classes:
              • class BaseDiscoveryProvider:
                - __init__(self)
                - name(self)
                - enabled(self)
                - enabled(self, value)
                - discover(self)
                - initialize(self)
                - shutdown(self)
                - refresh(self)
                - is_available(self)
                - __str__(self)
                - __repr__(self)
        📄 discovery_manager.py
            🏗️ Classes:
              • class DiscoveryManager:
                - __init__(self)
                - register(self, provider)
                - unregister(self, provider)
                - clear(self)
                - providers(self)
                - provider_count(self)
                - discover(self)
                - discover_provider(self, provider)
                - _deduplication_key(source)
                - __len__(self)
                - __iter__(self)
                - __repr__(self)
        📄 discovery_result.py
            🏗️ Classes:
              • class DiscoveryStatistics:
                - total_providers(self)
                - total_sources(self)
              • class DiscoveryResult:
                - complete(self)
                - add_source(self, source)
                - extend_sources(self, sources)
                - add_provider(self, provider_name)
                - add_warning(self, message)
                - add_error(self, message)
                - success(self)
                - has_warnings(self)
                - has_errors(self)
                - source_count(self)
                - provider_count(self)
                - __len__(self)
                - __bool__(self)
                - __repr__(self)
        📂 providers/
          📄 __init__.py
          📄 local_directory_provider.py
              🏗️ Classes:
                • class LocalDirectoryProvider:
                  - __init__(self, *directories)
                  - directories(self)
                  - recursive(self)
                  - discover(self)
                  - __repr__(self)
        📂 registry/
          📄 __init__.py
          📄 discovery_registry.py
              🏗️ Classes:
                • class DiscoveryRegistry:
                  - __init__(self)
                  - register(self, provider)
                  - unregister(self, name)
                  - clear(self)
                  - get(self, name)
                  - require(self, name)
                  - contains(self, name)
                  - providers(self)
                  - enabled_providers(self)
                  - disabled_providers(self)
                  - provider_names(self)
                  - count(self)
                  - is_empty(self)
                  - register_many(self, providers)
                  - enable_all(self)
                  - disable_all(self)
                  - __len__(self)
                  - __iter__(self)
                  - __contains__(self, name)
                  - __repr__(self)
      📂 downloaders/
        📄 __init__.py
        📄 base_downloader.py
            🏗️ Classes:
              • class BaseDownloader:
                - __init__(self)
                - name(self)
                - supports(self, manifest)
                - download(self, manifest)
                - prepare_directory(self, directory)
                - validate_destination(self, directory)
                - destination_file(self, manifest, filename)
                - remove_existing(self, path, overwrite)
                - finalize_result(self, result)
                - __repr__(self)
        📄 http_downloader.py
            🏗️ Classes:
              • class HTTPDownloader:
                - supports(self, manifest)
                - download(self, manifest)
                - _download_single(self, manifest, url)
                - _filename_from_url(url, expected)
                - _format_exception(exc)
                - __repr__(self)
        📄 local_file_importer.py
            🏗️ Classes:
              • class LocalFileImporter:
                - supports(self, manifest)
                - download(self, manifest)
                - _copy_file(self, source, manifest)
                - _copy_directory(self, source, manifest)
                - __repr__(self)
      📂 factories/
        📄 __init__.py
        📄 corpus_source_factory.py
            🏗️ Classes:
              • class CorpusSourceFactory:
                - from_file(cls, path)
                - from_url(cls, url)
                - from_metadata(cls)
                - is_supported(path)
                - __repr__(self)
      📂 importers/
        📄 base_importer.py
            🏗️ Classes:
              • class BaseImporter:
                - __init__(self)
                - identifier(self)
                - display_name(self)
                - supported_extensions(self)
                - import_file(self, file, **kwargs)
                - _import(self, **kwargs)
                - validate_file(self, file)
                - create_result(self, file)
                - read_text(self, file)
                - read_bytes(self, file)
                - supports(self, file)
                - encoding(self)
                - metadata(self)
                - __repr__(self)
        📄 html_importer.py
            🏗️ Classes:
              • class _TextExtractor:
                - __init__(self)
                - handle_starttag(self, tag, attrs)
                - handle_endtag(self, tag)
                - handle_data(self, data)
                - text(self)
              • class HtmlImporter:
                - identifier(self)
                - display_name(self)
                - supported_extensions(self)
                - _import(self, **kwargs)
                - _paragraphs(text)
                - metadata(self)
                - __repr__(self)
        📄 import_manager.py
            🏗️ Classes:
              • class ImportManager:
                - __init__(self)
                - register(self, importer)
                - unregister(self, extension)
                - importer_for(self, file)
                - import_file(self, file, **kwargs)
                - import_files(self, files, **kwargs)
                - import_directory(self, directory, **kwargs)
                - supports(self, file)
                - supported_extensions(self)
                - importer_count(self)
                - importers(self)
                - metadata(self)
                - clear(self)
                - __contains__(self, extension)
                - __len__(self)
                - __repr__(self)
        📄 import_result.py
        📄 pdf_importer.py
            🏗️ Classes:
              • class PdfImporter:
                - identifier(self)
                - display_name(self)
                - supported_extensions(self)
                - _import(self, **kwargs)
                - _load_reader()
                - metadata(self)
                - __repr__(self)
        📄 tei_importer.py
            🏗️ Classes:
              • class TeiImporter:
                - identifier(self)
                - display_name(self)
                - supported_extensions(self)
                - _import(self, **kwargs)
                - _find_first_text(self, root, tag_name)
                - metadata(self)
                - __repr__(self)
        📄 txt_importer.py
            🏗️ Classes:
              • class TxtImporter:
                - identifier(self)
                - display_name(self)
                - supported_extensions(self)
                - _import(self, **kwargs)
                - _split_into_units(text)
                - metadata(self)
                - __repr__(self)
        📄 xml_importer.py
            🏗️ Classes:
              • class XmlImporter:
                - identifier(self)
                - display_name(self)
                - supported_extensions(self)
                - _import(self, **kwargs)
                - _walk(self, element, depth)
                - _namespace(tag)
                - _local_name(tag)
                - metadata(self)
                - __repr__(self)
      📂 knowledge/
        📄 abstract_lexical_manifest.py
            🏗️ Classes:
              • class AbstractLexicalManifest:
                - identifier(self)
                - summary(self)
                - display_name(self)
                - has_download(self)
                - has_local_copy(self)
                - __str__(self)
        📄 abstract_lexical_parser.py
            🏗️ Classes:
              • class AbstractLexicalParser:
                - parse(self, source)
                - iter_records(self, source)
                - parse_record(self, record)
                - summary(self)
                - identifier(self)
                - __str__(self)
        📄 abstract_lexical_repository.py
            🏗️ Classes:
              • class AbstractLexicalRepository:
                - add(self, record)
                - add_all(self, records)
                - get(self, headword)
                - contains(self, headword)
                - all(self)
                - clear(self)
                - __iter__(self)
                - __len__(self)
                - count(self)
                - summary(self)
                - identifier(self)
                - __str__(self)
        📄 abstract_lexical_transformer.py
            🏗️ Classes:
              • class AbstractLexicalTransformer:
                - transform(self, entry)
                - transform_all(self, entries)
                - summary(self)
                - identifier(self)
                - __str__(self)
        📄 canonical_knowledge_repository.py
            🏗️ Classes:
              • class CanonicalKnowledgeRepository:
                - __post_init__(self)
                - services(self)
                - lexical(self)
                - dhatu(self)
                - morphology(self)
                - sandhi(self)
                - samasa(self)
                - semantic(self)
                - repository_count(self)
                - service_count(self)
                - component_count(self)
                - __len__(self)
        📄 knowledge_service_registry.py
            🏗️ Classes:
              • class KnowledgeServiceRegistry:
                - repository_count(self)
                - service_count(self)
                - component_count(self)
                - lexical(self)
                - dhatu(self)
                - morphology(self)
                - sandhi(self)
                - samasa(self)
                - semantic(self)
                - __len__(self)
        📄 monier_williams_manifest.py
            🏗️ Classes:
              • class MonierWilliamsManifest:
                - identifier(self)
                - summary(self)
                - __str__(self)
        📂 builders/
          📄 canonical_index_builder.py
              🏗️ Classes:
                • class CanonicalIndexBuilder:
                  - build(self, lexicons)
                  - _index_lexicon(self, lexicon)
                  - _index_entry(self, entry)
                  - _index_sense(self, sense)
                  - clear(self)
                  - summary(self)
                  - __str__(self)
          📄 canonical_knowledge_repository_builder.py
              🏗️ Classes:
                • class CanonicalKnowledgeRepositoryBuilder:
                  - build(self, lexicons)
                  - _populate_registries(self, lexicons)
                  - _synchronize_indexes(self)
                  - add_lexicon(self, lexicon)
                  - clear(self)
                  - summary(self)
                  - __str__(self)
        📂 connectors/
          📄 abstract_lexical_connector.py
              🏗️ Classes:
                • class AbstractLexicalConnector:
                  - discover(self)
                  - acquire(self, destination)
                  - parse(self, source)
                  - transform(self, parsed)
                  - validate(self, transformed)
                  - publish(self, transformed)
                  - execute(self, destination)
                  - summary(self)
                  - __str__(self)
        📂 indexes/
          📄 context_index.py
              🏗️ Classes:
                • class ContextIndex:
                  - add(self, context, sense)
                  - lookup(self, context_identifier)
                  - clear(self)
                  - context_count(self)
                  - summary(self)
                  - __contains__(self, context_identifier)
                  - __len__(self)
                  - __iter__(self)
                  - __str__(self)
          📄 headword_index.py
              🏗️ Classes:
                • class HeadwordIndex:
                  - add(self, entry)
                  - build(self, entries)
                  - clear(self)
                  - lookup(self, headword)
                  - prefix_search(self, prefix)
                  - all_entries(self)
                  - headwords(self)
                  - summary(self)
                  - __len__(self)
                  - __iter__(self)
                  - __contains__(self, headword)
                  - __str__(self)
          📄 knowledge_index.py
              🏗️ Classes:
                • class KnowledgeIndex:
                  - clear(self)
                  - summary(self)
                  - __str__(self)
          📄 lemma_index.py
              🏗️ Classes:
                • class LemmaIndex:
                  - add(self, lemma)
                  - build(self, lemmas)
                  - clear(self)
                  - lookup(self, lemma_id)
                  - lookup_text(self, text)
                  - all(self)
                  - lemma_ids(self)
                  - lemma_texts(self)
                  - summary(self)
                  - __len__(self)
                  - __iter__(self)
                  - __contains__(self, lemma_id)
                  - __str__(self)
          📄 source_index.py
              🏗️ Classes:
                • class SourceIndex:
                  - add(self, source, sense)
                  - lookup(self, source_id)
                  - clear(self)
                  - source_count(self)
                  - summary(self)
                  - __contains__(self, source_id)
                  - __len__(self)
                  - __iter__(self)
                  - __str__(self)
        📂 lookup/
          📄 lexical_lookup_engine.py
              🏗️ Classes:
                • class LexicalLookupEngine:
                  - lookup_headword(self, headword)
                  - prefix_search(self, prefix)
                  - lookup_lemma(self, lemma_id)
                  - lookup_lemma_text(self, lemma_text)
                  - lookup_context(self, context_id)
                  - contexts_for_purana(self, purana_name)
                  - contexts_for_chapter(self, chapter_identifier)
                  - contexts_for_sloka(self, sloka_identifier)
                  - lookup_source(self, source_id)
                  - lookup_source_name(self, source_name)
                  - lookup_source_short_name(self, short_name)
                  - search(self, query)
                  - summary(self)
                  - __str__(self)
        📂 models/
          📄 canonical_context.py
              🏗️ Classes:
                • class CanonicalContext:
                  - identifier(self)
                  - summary(self)
                  - __str__(self)
          📄 canonical_dictionary_entry.py
              🏗️ Classes:
                • class CanonicalDictionaryEntry:
                  - sense_count(self)
                  - display_name(self)
                  - has_transliteration(self)
                  - has_multiple_senses(self)
                  - primary_sense(self)
                  - summary(self)
                  - __len__(self)
                  - __iter__(self)
                  - __str__(self)
          📄 canonical_dictionary_sense.py
              🏗️ Classes:
                • class CanonicalDictionarySense:
                  - has_context(self)
                  - has_source(self)
                  - has_grammar(self)
                  - identifier(self)
                  - summary(self)
                  - __str__(self)
          📄 canonical_etymology.py
              🏗️ Classes:
                • class CanonicalEtymology:
                  - has_dhatu(self)
                  - has_pratyaya(self)
                  - reference_count(self)
                  - summary(self)
                  - __str__(self)
          📄 canonical_example.py
              🏗️ Classes:
                • class CanonicalExample:
                  - has_translation(self)
                  - has_context(self)
                  - reference_count(self)
                  - summary(self)
                  - __str__(self)
          📄 canonical_lemma.py
              🏗️ Classes:
                • class CanonicalLemma:
                  - summary(self)
                  - display_name(self)
                  - __str__(self)
          📄 canonical_lexical_record.py
              🏗️ Classes:
                • class CanonicalLexicalRecord:
                  - summary(self)
                  - __str__(self)
          📄 canonical_lexicon.py
              🏗️ Classes:
                • class CanonicalLexicon:
                  - entry_count(self)
                  - contains(self, headword)
                  - get(self, headword)
                  - all_entries(self)
                  - all_senses(self)
                  - all_contexts(self)
                  - all_sources(self)
                  - sense_count(self)
                  - summary(self)
                  - __len__(self)
                  - __iter__(self)
                  - __str__(self)
          📄 canonical_reference.py
              🏗️ Classes:
                • class CanonicalReference:
                  - location(self)
                  - summary(self)
                  - __str__(self)
          📄 canonical_source.py
              🏗️ Classes:
                • class CanonicalSource:
                  - display_name(self)
                  - is_online(self)
                  - is_lexicon(self)
                  - is_primary_text(self)
                  - is_grammar(self)
                  - summary(self)
                  - __str__(self)
          📄 raw_lexical_entry.py
              🏗️ Classes:
                • class RawLexicalEntry:
                  - has_headword(self)
                  - has_raw_text(self)
                  - summary(self)
                  - __str__(self)
        📂 parsers/
          📄 monier_williams_parser.py
              🏗️ Classes:
                • class MonierWilliamsParser:
                  - parse(self, source)
                  - iter_records(self, source)
                  - parse_record(self, record)
                  - extract_headword(self, record)
                  - summary(self)
                  - __str__(self)
        📂 pipelines/
          📄 abstract_lexical_pipeline.py
              🏗️ Classes:
                • class AbstractLexicalPipeline:
                  - execute(self)
                  - before_pipeline(self)
                  - after_pipeline(self)
                  - connect(self)
                  - fetch(self)
                  - parse(self, resource)
                  - transform(self, raw_entries)
                  - validate(self, canonical_records)
                  - persist(self, canonical_records)
                  - build_manifest(self, persisted_objects)
                  - report(self)
                  - summary(self)
                  - __str__(self)
          📄 monier_williams_pipeline.py
              🏗️ Classes:
                • class MonierWilliamsPipeline:
                  - validate(self, canonical_records)
                  - build_manifest(self, persisted_objects)
        📂 registries/
          📄 lemma_registry.py
              🏗️ Classes:
                • class LemmaRegistry:
                  - register(self, lemma)
                  - lookup(self, lemma_id)
                  - lookup_by_text(self, text)
                  - all(self)
                  - lemma_ids(self)
                  - summary(self)
                  - __len__(self)
                  - __iter__(self)
                  - __contains__(self, lemma_id)
                  - __str__(self)
          📄 lexical_registry.py
              🏗️ Classes:
                • class LexicalRegistry:
                  - register(self, lexicon)
                  - lookup(self, lexicon_id)
                  - lookup_by_name(self, name)
                  - all(self)
                  - lexicon_ids(self)
                  - summary(self)
                  - __len__(self)
                  - __iter__(self)
                  - __contains__(self, lexicon_id)
                  - __str__(self)
          📄 source_registry.py
              🏗️ Classes:
                • class SourceRegistry:
                  - register(self, source)
                  - lookup(self, source_id)
                  - lookup_by_name(self, name)
                  - lookup_by_short_name(self, short_name)
                  - all(self)
                  - source_ids(self)
                  - summary(self)
                  - __len__(self)
                  - __iter__(self)
                  - __contains__(self, source_id)
                  - __str__(self)
        📂 repositories/
          📄 canonical_lexical_repository.py
              🏗️ Classes:
                • class CanonicalLexicalRepository:
                  - add(self, record)
                  - add_all(self, records)
                  - contains(self, headword)
                  - get(self, headword)
                  - headwords(self)
                  - records(self)
                  - headword_count(self)
                  - record_count(self)
                  - summary(self)
                  - __contains__(self, headword)
                  - __len__(self)
                  - __iter__(self)
                  - __str__(self)
        📂 transformers/
          📄 monier_williams_transformer.py
              🏗️ Classes:
                • class MonierWilliamsTransformer:
                  - transform(self, entry)
      📂 lexical/
        📄 __init__.py
        📂 monier_williams/
          📄 __init__.py
          📄 delimited_monier_williams_parser.py
              🏗️ Classes:
                • class DelimitedMonierWilliamsParser:
                  - __init__(self)
                  - parse(self, source_text)
                  - parse_lines(self, lines)
                  - iter_parse(self, source_text)
                  - _validate_header(self, header)
                  - _normalize_header(value)
          📄 file_monier_williams_source.py
              🏗️ Classes:
                • class FileMonierWilliamsSource:
                  - __post_init__(self)
                  - identifier(self)
                  - source_name(self)
                  - exists(self)
                  - read(self)
          📄 local_monier_williams_source_acquirer.py
              🏗️ Classes:
                • class LocalMonierWilliamsSourceAcquirer:
                  - __init__(self, path)
                  - path(self)
                  - encoding(self)
                  - acquire(self)
          📄 monier_williams_acquisition_result.py
              🏗️ Classes:
                • class MonierWilliamsAcquisitionResult:
                  - __post_init__(self)
          📄 monier_williams_acquisition_service.py
              🏗️ Classes:
                • class MonierWilliamsAcquisitionService:
                  - read(self)
                  - acquire(self)
                  - count(self)
                  - _source_identifier(self)
                  - _source_name(self)
                  - _line_count(text)
          📄 monier_williams_parsed_entry.py
              🏗️ Classes:
                • class MonierWilliamsParsedEntry:
                  - __post_init__(self)
          📄 monier_williams_parser.py
              🏗️ Classes:
                • class MonierWilliamsParser:
                  - parse(self, source_text)
                  - parse_lines(self, lines)
          📄 monier_williams_parser_config.py
              🏗️ Classes:
                • class MonierWilliamsParserConfig:
          📄 monier_williams_source.py
              🏗️ Classes:
                • class MonierWilliamsSource:
                  - source(self)
                  - identifier(self)
                  - source_name(self)
                  - read(self)
                  - acquire(self)
          📄 monier_williams_source_acquirer.py
              🏗️ Classes:
                • class MonierWilliamsSourceAcquirer:
                  - acquire(self)
          📄 monier_williams_source_parser.py
              🏗️ Classes:
                • class _SourceProtocol:
                  - acquire(self)
                  - read(self)
                • class _ParserProtocol:
                  - parse(self, source_text)
                • class MonierWilliamsSourceParser:
                  - __init__(self, acquirer, parser)
                  - _read_source(self)
                  - _is_tagged_source(source_text)
                  - _create_default_parser(self, source_text)
                  - parse(self, source_text)
                  - parse_record(self, source_text)
                • class _TaggedMonierWilliamsParser:
                  - parse(self, source_text)
                  - _build_record(self, sequence, lines)
          📄 monier_williams_source_pipeline.py
              🏗️ Classes:
                • class MonierWilliamsSourcePipeline:
                  - run(self)
                  - parse(self)
                  - records(self)
                  - _parse_raw_text(text)
          📄 monier_williams_source_record.py
              🏗️ Classes:
                • class MonierWilliamsSourceRecord:
                  - __init__(self, sequence, raw_text, fields, **kwargs)
                  - headword(self)
                  - transliteration(self)
                  - definition(self)
                  - grammatical_label(self)
                  - grammatical_category(self)
                  - source(self)
                  - source_id(self)
                  - source_reference(self)
                  - homonym(self)
                  - get(self, key, default)
      📂 metadata/
        📄 __init__.py
        📄 base_metadata_extractor.py
            🏗️ Classes:
              • class BaseMetadataExtractor:
                - __init__(self)
                - extract(self, source)
                - validate(self, source)
                - extract_if_valid(self, source)
                - warnings(self)
                - errors(self)
                - has_warnings(self)
                - has_errors(self)
                - add_warning(self, message)
                - add_error(self, message)
                - clear_diagnostics(self)
                - capabilities(self)
                - supports(self, source)
                - __repr__(self)
        📄 extraction_result.py
            🏗️ Classes:
              • class ExtractionResult:
                - finish(self)
                - succeeded(self)
                - failed(self)
                - has_warnings(self)
                - duration_seconds(self)
                - add_metadata(self, key, value)
                - merge_metadata(self, metadata)
                - add_warning(self, message)
                - add_error(self, message)
                - increment_statistic(self, key, amount)
                - add_provenance(self, key, value)
                - to_dict(self)
                - __repr__(self)
        📄 metadata_manager.py
            🏗️ Classes:
              • class MetadataManager:
                - __init__(self)
                - register(self, extractor)
                - unregister(self, extractor)
                - clear(self)
                - extractors(self)
                - extract(self, source)
                - extract_many(self, sources)
                - extractor_count(self)
                - capabilities(self)
                - __len__(self)
                - __iter__(self)
                - __repr__(self)
        📂 extractors/
          📄 __init__.py
          📄 corpus_type_extractor.py
              🏗️ Classes:
                • class CorpusTypeExtractor:
                  - capabilities(self)
                  - extract(self, source)
                  - _build_search_text(self, source, metadata)
                  - _detect(self, searchable)
                  - __repr__(self)
          📄 language_extractor.py
              🏗️ Classes:
                • class LanguageExtractor:
                  - capabilities(self)
                  - extract(self, source)
                  - _load_text(self, source)
                  - _tokenize(self, text)
                  - _score_languages(self, text)
                  - __repr__(self)
          📄 numbering_extractor.py
              🏗️ Classes:
                • class NumberingExtractor:
                  - capabilities(self)
                  - extract(self, source)
                  - _load_text(self, source)
                  - _detect_levels(self, text)
                  - _detect_numbering(self, text)
                  - __repr__(self)
          📄 script_extractor.py
              🏗️ Classes:
                • class ScriptExtractor:
                  - capabilities(self)
                  - extract(self, source)
                  - _load_text(self, source)
                  - _count_scripts(self, text)
                  - _detect_character_script(self, ch)
                  - __repr__(self)
          📄 title_extractor.py
              🏗️ Classes:
                • class TitleExtractor:
                  - capabilities(self)
                  - extract(self, source)
                  - _extract_xml_title(self, text)
                  - _extract_html_title(self, text)
                  - _humanize(filename)
                  - __repr__(self)
          📄 work_identifier_extractor.py
              🏗️ Classes:
                • class WorkIdentifierExtractor:
                  - __init__(self, registry)
                  - capabilities(self)
                  - extract(self, source)
                  - _populate_result(self, result, work)
                  - _build_searchable_text(self, source, metadata)
                  - registry(self)
                  - __repr__(self)
        📂 models/
          📄 work_alias.py
              🏗️ Classes:
                • class WorkAlias:
                  - normalized(self)
                  - matches(self, text)
                  - __str__(self)
                  - __repr__(self)
          📄 work_definition.py
              🏗️ Classes:
                • class WorkDefinition:
                  - add_alias(self, alias)
                  - remove_alias(self, value)
                  - find_alias(self, text)
                  - matches(self, text)
                  - preferred_alias(self)
                  - alias_count(self)
                  - to_dict(self)
                  - from_dict(cls, data)
                  - __contains__(self, text)
                  - __len__(self)
                  - __repr__(self)
        📂 registries/
          📄 work_registry.py
              🏗️ Classes:
                • class WorkRegistry:
                  - __init__(self, registry_path)
                  - load(self)
                  - _validate_registry(data)
                  - find_work(self, text)
                  - get(self, identifier)
                  - exists(self, identifier)
                  - identifiers(self)
                  - titles(self)
                  - search(self, query)
                  - corpus_types(self)
                  - works_by_corpus_type(self, corpus_type)
                  - authors(self)
                  - __iter__(self)
                  - __contains__(self, identifier)
                  - __getitem__(self, identifier)
                  - __len__(self)
                  - registry_path(self)
                  - __repr__(self)
      📂 models/
        📄 acquisition_manifest.py
            🏗️ Classes:
              • class AcquisitionManifest:
                - add_url(self, url)
                - add_mirror(self, url)
                - all_urls(self)
                - set_metadata(self, key, value)
                - get_metadata(self, key, default)
                - has_urls(self)
                - requires_download(self)
                - requires_checksum_validation(self)
                - requires_license_validation(self)
                - to_dict(self)
                - __repr__(self)
        📄 acquisition_result.py
            🏗️ Classes:
              • class AcquisitionResult:
                - finalize(self)
                - mark_success(self, message)
                - add_warning(self, message)
                - add_error(self, message)
                - add_downloaded_file(self, path)
                - add_extracted_file(self, path)
                - set_metadata(self, key, value)
                - get_metadata(self, key, default)
                - has_errors(self)
                - has_warnings(self)
                - downloaded_file_count(self)
                - extracted_file_count(self)
                - to_dict(self)
                - __repr__(self)
        📄 corpus_source.py
            🏗️ Classes:
              • class CorpusSource:
                - has_download_url(self)
                - is_downloaded(self)
                - is_ready_for_import(self)
                - filename(self)
                - add_tag(self, tag)
                - remove_tag(self, tag)
                - has_tag(self, tag)
                - set_metadata(self, key, value)
                - get_metadata(self, key, default)
                - add_download_url(self, url)
                - update_status(self, status)
                - set_local_path(self, path)
                - to_dict(self)
                - __repr__(self)
        📄 source_format.py
            🏗️ Classes:
              • class SourceFormat:
                - is_text(self)
                - is_structured(self)
                - is_archive(self)
                - requires_ocr(self)
                - is_document(self)
                - from_extension(cls, extension)
                - __str__(self)
        📄 source_license.py
            🏗️ Classes:
              • class SourceLicense:
                - is_open(self)
                - requires_attribution(self)
                - allows_commercial_use(self)
                - requires_permission(self)
                - from_string(cls, value)
                - __str__(self)
        📄 source_status.py
            🏗️ Classes:
              • class SourceStatus:
                - is_terminal(self)
                - is_downloaded(self)
                - is_validated(self)
                - is_importable(self)
                - has_failed(self)
                - is_active(self)
                - from_string(cls, value)
                - __str__(self)
        📄 source_type.py
            🏗️ Classes:
              • class SourceType:
                - is_lexical(self)
                - is_corpus(self)
                - is_reference(self)
                - from_string(cls, value)
                - __str__(self)
      📂 normalizers/
        📄 __init__.py
        📄 base_normalizer.py
            🏗️ Classes:
              • class BaseNormalizer:
                - __init__(self)
                - name(self)
                - normalize(self, text)
                - normalize_lines(self, lines)
                - normalize_file(self, path)
                - ensure_text(text)
                - is_empty(text)
                - has_content(text)
                - __str__(self)
                - __repr__(self)
        📄 composite_normalizer.py
            🏗️ Classes:
              • class CompositeNormalizer:
                - __init__(self, normalizers)
                - normalize(self, text)
                - add(self, normalizer)
                - extend(self, normalizers)
                - clear(self)
                - normalizers(self)
                - count(self)
                - is_empty(self)
                - __len__(self)
                - __iter__(self)
                - __getitem__(self, index)
                - __repr__(self)
        📄 line_ending_normalizer.py
            🏗️ Classes:
              • class LineEndingNormalizer:
                - __init__(self, newline)
                - newline(self)
                - normalize(self, text)
                - normalize_string(text, newline)
                - detect_style(text)
                - __repr__(self)
        📄 sanskrit_normalizer.py
            🏗️ Classes:
              • class SanskritNormalizer:
                - __init__(self)
                - normalize(self, text)
                - _normalize_dandas(self, text)
                - _normalize_avagraha(self, text)
                - _normalize_hyphens(self, text)
                - _normalize_quotes(self, text)
                - _remove_duplicate_punctuation(self, text)
                - preserve_vedic_accents(self)
                - preserve_punctuation(self)
                - __repr__(self)
        📄 unicode_normalizer.py
            🏗️ Classes:
              • class UnicodeNormalizationForm:
              • class UnicodeNormalizer:
                - __init__(self, normalization_form)
                - normalization_form(self)
                - normalize(self, text)
                - _remove_characters(self, text)
                - _normalize_spaces(self, text)
                - _normalize_line_separators(self, text)
                - _remove_control_characters(self, text)
                - is_normalized(text, form)
                - normalize_string(text, form)
                - __repr__(self)
        📄 whitespace_normalizer.py
            🏗️ Classes:
              • class WhitespaceNormalizer:
                - __init__(self)
                - tab_size(self)
                - strip_leading(self)
                - strip_trailing(self)
                - collapse_blank_lines(self)
                - normalize(self, text)
                - _collapse_blank_lines_fn(self, text)
                - normalize_string(text, **kwargs)
                - __repr__(self)
      📂 parsers/
        📄 __init__.py
        📄 base_catalog_parser.py
            🏗️ Classes:
              • class BaseCatalogParser:
                - __init__(self)
                - parse(self, content)
                - validate(self, content)
                - parse_if_valid(self, content)
                - warnings(self)
                - errors(self)
                - has_warnings(self)
                - has_errors(self)
                - add_warning(self, message)
                - add_error(self, message)
                - clear_diagnostics(self)
                - metadata(self)
                - __repr__(self)
        📄 gretil_catalog_parser.py
            🏗️ Classes:
              • class _GretilHTMLParser:
                - __init__(self)
                - handle_starttag(self, tag, attrs)
                - handle_data(self, data)
                - handle_endtag(self, tag)
              • class GretilCatalogParser:
                - __init__(self)
                - parse(self, content)
                - validate(self, content)
                - _is_supported(self, href)
                - _title_from_href(href)
                - metadata(self)
                - __repr__(self)
      📂 pipelines/
        📄 acquisition_pipeline.py
            🏗️ Classes:
              • class AcquisitionPipeline:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - acquire(self, manifest)
                - run(self, manifest)
                - __str__(self)
      📂 providers/
        📄 acquisition_request.py
            🏗️ Classes:
              • class AcquisitionRequest:
                - has_query(self)
                - has_work_identifier(self)
                - has_destination(self)
                - allows_extension(self, extension)
                - option(self, name, default)
                - metadata(self, name, default)
                - __repr__(self)
        📄 acquisition_response.py
            🏗️ Classes:
              • class AcquisitionResponse:
                - add_resource(self, resource)
                - add_download(self, file)
                - skip(self, resource)
                - warning(self, message)
                - error(self, message)
                - set_metadata(self, key, value)
                - increment(self, name, amount)
                - finish(self)
                - duration_seconds(self)
                - has_errors(self)
                - has_warnings(self)
                - resource_count(self)
                - download_count(self)
                - merge(self, other)
                - __len__(self)
                - __bool__(self)
                - __repr__(self)
        📄 base_provider.py
            🏗️ Classes:
              • class BaseProvider:
                - __init__(self)
                - identifier(self)
                - display_name(self)
                - homepage(self)
                - supports_discovery(self)
                - supports_download(self)
                - supports_search(self)
                - supports_metadata(self)
                - supports_incremental_updates(self)
                - discover(self, request)
                - acquire(self, request)
                - health_check(self)
                - capabilities(self)
                - validate_request(self, request)
                - create_response(self)
                - timeout(self)
                - cache_directory(self)
                - provider_metadata(self)
                - __repr__(self)
        📄 cologne_provider.py
            🏗️ Classes:
              • class CologneProvider:
                - __init__(self, repository)
                - identifier(self)
                - display_name(self)
                - corpus_name(self)
                - publisher(self)
                - primary_encoding(self)
                - preferred_formats(self)
                - supports_lexicons(self)
                - supports_dictionaries(self)
                - supports_word_indices(self)
                - metadata(self)
                - health_check(self)
                - __repr__(self)
        📄 github_provider.py
            🏗️ Classes:
              • class GitHubProvider:
                - __init__(self, repository)
                - identifier(self)
                - display_name(self)
                - discover(self, request)
                - acquire(self, request)
                - supported_extensions(self)
                - supports_extension(self, extension)
                - metadata(self)
                - health_check(self)
                - __repr__(self)
        📄 gretil_provider.py
            🏗️ Classes:
              • class GretilProvider:
                - __init__(self, repository_client, parser, **kwargs)
                - identifier(self)
                - display_name(self)
                - homepage(self)
                - discover(self, request)
                - acquire(self, request)
                - health_check(self)
                - _filter_entries(entries, query)
                - repository_client(self)
                - parser(self)
                - __repr__(self)
        📄 internet_archive_provider.py
            🏗️ Classes:
              • class InternetArchiveProvider:
                - __init__(self, repository)
                - identifier(self)
                - display_name(self)
                - discover(self, request)
                - acquire(self, request)
                - supported_extensions(self)
                - supports_extension(self, extension)
                - metadata(self)
                - health_check(self)
                - preferred_formats(self)
                - __repr__(self)
        📄 muktabodha_provider.py
            🏗️ Classes:
              • class MuktabodhaProvider:
                - __init__(self, repository)
                - identifier(self)
                - display_name(self)
                - corpus_name(self)
                - publisher(self)
                - primary_encoding(self)
                - preferred_formats(self)
                - supports_tantra(self)
                - supports_agama(self)
                - supports_shaiva(self)
                - supports_shakta(self)
                - supports_unicode(self)
                - metadata(self)
                - health_check(self)
                - __repr__(self)
        📄 provider_registry.py
            🏗️ Classes:
              • class ProviderRegistry:
                - __init__(self)
                - register(self, provider)
                - unregister(self, identifier)
                - provider(self, identifier)
                - exists(self, identifier)
                - identifiers(self)
                - providers(self)
                - metadata(self)
                - health_report(self)
                - __contains__(self, identifier)
                - __iter__(self)
                - __len__(self)
                - __repr__(self)
        📄 sanskritdocuments_provider.py
            🏗️ Classes:
              • class SanskritDocumentsProvider:
                - __init__(self, repository)
                - identifier(self)
                - display_name(self)
                - discover(self, request)
                - acquire(self, request)
                - supported_extensions(self)
                - preferred_formats(self)
                - supports_extension(self, extension)
                - metadata(self)
                - health_check(self)
                - __repr__(self)
        📄 sarit_provider.py
            🏗️ Classes:
              • class SaritProvider:
                - __init__(self, repository)
                - identifier(self)
                - display_name(self)
                - preferred_formats(self)
                - corpus_name(self)
                - publisher(self)
                - primary_encoding(self)
                - metadata(self)
                - health_check(self)
                - __repr__(self)
        📄 xml_corpus_provider.py
            🏗️ Classes:
              • class XmlCorpusProvider:
                - __init__(self, repository)
                - discover(self, request)
                - acquire(self, request)
                - supported_extensions(self)
                - preferred_formats(self)
                - supports_extension(self, extension)
                - metadata(self)
                - health_check(self)
                - __repr__(self)
      📂 registry/
        📄 __init__.py
        📄 source_catalog.py
            🏗️ Classes:
              • class SourceCatalog:
                - __init__(self, sources)
                - add(self, source)
                - remove(self, source_id)
                - clear(self)
                - get(self, source_id)
                - require(self, source_id)
                - contains(self, source_id)
                - by_type(self, source_type)
                - by_status(self, status)
                - enabled(self)
                - ids(self)
                - values(self)
                - items(self)
                - size(self)
                - is_empty(self)
                - __contains__(self, source_id)
                - __len__(self)
                - __iter__(self)
                - __repr__(self)
        📄 source_registry.py
            🏗️ Classes:
              • class SourceRegistry:
                - __init__(self, catalog)
                - catalog(self)
                - register(self, source)
                - unregister(self, source_id)
                - is_registered(self, source_id)
                - get(self, source_id)
                - require(self, source_id)
                - all_sources(self)
                - sources_by_type(self, source_type)
                - register_many(self, sources)
                - discover(self)
                - load_manifest(self, path)
                - save_manifest(self, manifest, path)
                - load_registry(self, path)
                - save_registry(self, path)
                - source_count(self)
                - is_empty(self)
                - __len__(self)
                - __iter__(self)
                - __repr__(self)
      📂 repositories/
        📄 __init__.py
        📄 base_repository_client.py
            🏗️ Classes:
              • class BaseRepositoryClient:
                - __init__(self, downloader)
                - identifier(self)
                - base_url(self)
                - catalog_url(self)
                - ping(self)
                - fetch_catalog(self)
                - resource_url(self, resource)
                - download_resource(self, resource, destination_directory)
                - downloader(self)
                - metadata(self)
                - __repr__(self)
        📄 default_source_repository.py
            🏗️ Classes:
              • class DefaultSourceRepository:
                - add(self, source)
                - get(self, source_id)
                - exists(self, source_id)
                - all(self)
                - remove(self, source_id)
                - clear(self)
                - __contains__(self, source_id)
                - __len__(self)
                - __iter__(self)
                - __repr__(self)
        📄 gretil_repository_client.py
            🏗️ Classes:
              • class GretilRepositoryClient:
                - identifier(self)
                - base_url(self)
                - catalog_url(self)
                - fetch_catalog(self)
                - resource_url(self, resource)
                - catalog_metadata(self)
                - supports_https(self)
                - __str__(self)
                - __repr__(self)
        📄 remote_repository_client.py
            🏗️ Classes:
              • class RemoteRepositoryClient:
                - __init__(self)
                - base_url(self)
                - timeout(self)
                - session(self)
                - get(self, url, **kwargs)
                - get_text(self, url, encoding)
                - get_bytes(self, url)
                - download(self, url, destination)
                - build_url(self, *parts)
                - discover(self)
                - ping(self)
                - close(self)
                - __enter__(self)
                - __exit__(self, exc_type, exc, tb)
                - __repr__(self)
        📄 repository_registry.py
            🏗️ Classes:
              • class RepositoryRegistry:
                - __init__(self)
                - register(self, repository)
                - unregister(self, identifier)
                - get(self, identifier)
                - require(self, identifier)
                - exists(self, identifier)
                - identifiers(self)
                - repositories(self)
                - metadata(self)
                - health_report(self)
                - healthy_repositories(self)
                - clear(self)
                - __contains__(self, identifier)
                - __getitem__(self, identifier)
                - __iter__(self)
                - __len__(self)
                - __repr__(self)
        📄 source_repository.py
            🏗️ Classes:
              • class SourceRepository:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - get(self, identifier)
                - exists(self, identifier)
                - all(self)
                - add(self, source)
                - remove(self, identifier)
                - count(self)
                - is_empty(self)
                - __len__(self)
                - __contains__(self, identifier)
                - __str__(self)
      📂 services/
        📄 acquisition_service.py
            🏗️ Classes:
              • class AcquisitionService:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - acquire(self, manifest)
                - run(self, manifest)
                - __str__(self)
        📄 default_acquisition_service.py
            🏗️ Classes:
              • class DefaultAcquisitionService:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - acquire(self, manifest)
                - run(self, manifest)
                - __str__(self)
      📂 sources/
        📄 __init__.py
        📄 monier_williams.py
            🏗️ Classes:
              • class MonierWilliamsSource:
                - identity(self)
        📄 monier_williams_manifest.py
            🔹 Constants:
              • MW_SOURCE_URL
            ⚙️ Functions:
              • create_monier_williams_manifest()
      📂 validators/
        📄 __init__.py
        📄 base_validator.py
            🏗️ Classes:
              • class BaseValidator:
                - __init__(self)
                - name(self)
                - supports(self, manifest)
                - validate(self, manifest, result)
                - require_downloads(self, result)
                - require_file(self, path)
                - add_warning(self, result, message)
                - add_error(self, result, message)
                - __repr__(self)
        📄 checksum_validator.py
            🏗️ Classes:
              • class ChecksumValidator:
                - supports(self, manifest)
                - validate(self, manifest, result)
                - _compute_checksum(self, path, algorithm_factory)
                - supported_algorithms(cls)
                - __repr__(self)
        📄 file_validator.py
            🏗️ Classes:
              • class FileValidator:
                - supports(self, manifest)
                - validate(self, manifest, result)
                - _validate_file(self, path, manifest, result)
                - _validate_readable(self, path)
                - _validate_size(self, path)
                - _validate_filename(self, path, manifest, result)
                - _validate_extension(self, path, manifest, result)
                - is_empty(path)
                - file_size(path)
                - __repr__(self)
    📂 ai/
      📄 __init__.py
      📄 agent.py
          🏗️ Classes:
            • class Agent:
              - __init__(self, strategy, reasoner, tools)
              - strategy(self)
              - reasoner(self)
              - tools(self)
              - tool_count(self)
              - has_tools(self)
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - execute(self, context)
      📄 agent_strategy.py
          🏗️ Classes:
            • class AgentStrategy:
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - execute(self, context)
      📄 ai_model.py
          🏗️ Classes:
            • class AIModel:
              - identifier(self)
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - provider(self)
              - family(self)
              - version(self)
              - capabilities(self)
              - capability_count(self)
              - has_capabilities(self)
              - supports(self, capability)
              - __str__(self)
      📄 ai_model_collection.py
          🏗️ Classes:
            • class AIModelCollection:
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - size(self)
              - is_empty(self)
              - contains(self, model)
              - add(self, model)
              - __iter__(self)
              - __len__(self)
              - __str__(self)
      📄 ai_model_metadata.py
          🏗️ Classes:
            • class AIModelMetadata:
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - has_family(self)
              - has_version(self)
              - capability_count(self)
              - has_capabilities(self)
              - supports(self, capability)
              - __str__(self)
      📄 ai_provider.py
          🏗️ Classes:
            • class AIProvider:
              - identifier(self)
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - organization(self)
              - website(self)
              - capability_count(self)
              - model_count(self)
              - supports(self, capability)
              - __str__(self)
      📄 ai_provider_metadata.py
          🏗️ Classes:
            • class AIProviderMetadata:
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - has_organization(self)
              - has_website(self)
              - capability_count(self)
              - has_capabilities(self)
              - supports(self, capability)
              - __str__(self)
      📄 ai_request.py
          🏗️ Classes:
            • class AIRequest:
              - identifier(self)
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - parameter(self, name, default)
              - __str__(self)
      📄 ai_response.py
          🏗️ Classes:
            • class AIResponse:
              - identifier(self)
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - model(self)
              - prompt(self)
              - is_success(self)
              - is_failure(self)
              - __str__(self)
      📄 conversation.py
          🏗️ Classes:
            • class Conversation:
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - is_empty(self)
              - prompt_count(self)
              - add_prompt(self, prompt)
              - __iter__(self)
              - __len__(self)
              - __str__(self)
      📄 default_agent.py
          🏗️ Classes:
            • class DefaultAgent:
              - execute(self, context)
      📄 default_reasoner.py
          🏗️ Classes:
            • class DefaultReasoner:
              - reason(self, context)
      📄 default_reasoning_strategy.py
          🏗️ Classes:
            • class DefaultReasoningStrategy:
              - __init__(self, inference_engine)
              - inference_engine(self)
              - reason(self, context)
      📄 embedding_model.py
          🏗️ Classes:
            • class EmbeddingModel:
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - embed(self, text)
      📄 explainer_.py
          ⚙️ Functions:
            • explain_result(result)
      📄 inference_context.py
          🏗️ Classes:
            • class InferenceContext:
              - identifier(self)
              - model(self)
              - prompt(self)
              - parameters(self)
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - __str__(self)
      📄 inference_result.py
          🏗️ Classes:
            • class InferenceResult:
              - identifier(self)
              - request(self)
              - model(self)
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - is_success(self)
              - is_failure(self)
              - content(self)
              - __str__(self)
      📄 knowledge_context.py
          🏗️ Classes:
            • class KnowledgeContext:
              - identifier(self)
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - item_count(self)
              - is_empty(self)
              - has_items(self)
              - items(self)
              - __iter__(self)
              - __len__(self)
              - __str__(self)
      📄 knowledge_retriever.py
          🏗️ Classes:
            • class KnowledgeRetriever:
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - retrieve(self, query)
      📄 memory.py
          🏗️ Classes:
            • class Memory:
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - item_count(self)
              - is_empty(self)
              - has_items(self)
              - add_item(self, item)
              - __iter__(self)
              - __len__(self)
              - __str__(self)
      📄 prompt.py
          🏗️ Classes:
            • class Prompt:
              - identifier(self)
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - variables(self)
              - variable_count(self)
              - has_variables(self)
              - value(self, name, default)
              - __str__(self)
      📄 prompt_template.py
          🏗️ Classes:
            • class PromptTemplate:
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - variable_count(self)
              - has_variables(self)
              - supports(self, variable)
              - __str__(self)
      📄 reasoner.py
          🏗️ Classes:
            • class Reasoner:
              - __init__(self, strategy)
              - strategy(self)
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - reason(self, context)
      📄 reasoning_context.py
          🏗️ Classes:
            • class ReasoningContext:
              - identifier(self)
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - prompt_count(self)
              - is_empty(self)
              - configuration(self)
              - services(self)
              - plugins(self)
              - resources(self)
              - events(self)
              - __str__(self)
      📄 reasoning_strategy.py
          🏗️ Classes:
            • class ReasoningStrategy:
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - reason(self, context)
      📄 tool.py
          🏗️ Classes:
            • class Tool:
              - identifier(self)
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - execute(self, context)
      📄 translator_.py
          ⚙️ Functions:
            • translate_literal(tokens)
      📄 vector_store.py
          🏗️ Classes:
            • class VectorStore:
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - add(self, identifier, embedding)
              - search(self, embedding, limit)
    📂 amarakosha/
      📄 __init__.py
      📂 builders/
        📄 base_amarakosha_builder.py
            🏗️ Classes:
              • class BaseAmarakoshaBuilder:
        📄 base_knowledge_record_builder.py
            🏗️ Classes:
              • class BaseKnowledgeRecordBuilder:
                - record_type(self)
                - normalize_text(self, text)
                - normalize_optional(self, text)
        📄 synset_builder.py
            🏗️ Classes:
              • class SynsetBuilder:
                - __init__(self)
                - with_identifier(self, identifier)
                - with_metadata(self, metadata)
                - add_lexeme(self, lexeme)
                - build(self)
        📄 synset_record_builder.py
            🏗️ Classes:
              • class SynsetRecordBuilder:
                - __init__(self)
                - record_type(self)
                - build(self, record)
        📄 varga_builder.py
            🏗️ Classes:
              • class VargaBuilder:
                - __init__(self)
                - with_identifier(self, identifier)
                - with_metadata(self, metadata)
                - add_synset(self, synset)
                - build(self)
      📂 enums/
        📄 Amarakanda.py
            🏗️ Classes:
              • class Amarakanda:
                - english_name(self)
                - devanagari(self)
                - iast(self)
                - order(self)
      📂 importers/
        📄 __init__.py
        📄 amarakosha_importer.py
            🏗️ Classes:
              • class AmarakoshaImporter:
                - __init__(self, parser, registry)
                - import_source(self, source)
      📂 models/
        📄 synset.py
            🏗️ Classes:
              • class Synset:
                - __init__(self, identifier, metadata, children)
                - lexemes(self)
                - kanda(self)
                - varga(self)
                - varga_number(self)
                - verse_number(self)
                - pada_number(self)
                - synset_identifier(self)
                - add_lexeme(self, lexeme)
                - remove_lexeme(self, lexeme)
        📄 synset_metadata.py
            🏗️ Classes:
              • class SynsetMetadata:
        📄 varga.py
            🏗️ Classes:
              • class Varga:
                - __init__(self, identifier, metadata, children)
                - synsets(self)
                - kanda(self)
                - varga_number(self)
                - name(self)
                - title(self)
                - add_synset(self, synset)
                - remove_synset(self, synset)
        📄 varga_metadata.py
            🏗️ Classes:
              • class VargaMetadata:
      📂 parsers/
        📄 __init__.py
        📄 amarakosha_parser.py
            🏗️ Classes:
              • class AmarakoshaParser:
                - knowledge_source(self)
                - parse(self, source)
                - parse_kanda(self, lines)
                - parse_varga(self, lines)
                - parse_synset(self, line)
        📄 base_knowledge_parser.py
            🏗️ Classes:
              • class BaseKnowledgeParser:
                - normalize_text(self, text)
                - normalize_optional(self, text)
                - parse_lines(self, lines)
                - subsystem(self)
                - knowledge_source(self)
      📂 records/
        📄 __init__.py
        📄 synset_record.py
            🏗️ Classes:
              • class SynsetRecord:
                - display_text(self)
        📄 varga_record.py
            🏗️ Classes:
              • class VargaRecord:
                - display_text(self)
      📂 registries/
        📄 __init__.py
        📄 amarakosha_registry.py
            🏗️ Classes:
              • class AmarakoshaRegistry:
                - register_many(self, objects)
                - vargas(self)
                - synsets(self)
      📂 validators/
        📄 base_knowledge_validator.py
            🏗️ Classes:
              • class BaseKnowledgeValidator:
        📄 synset_validator.py
            🏗️ Classes:
              • class SynsetValidator:
                - validate(self, obj)
    📂 analysis/
      📄 __init__.py
      📄 grammar.py
          ⚙️ Functions:
            • summarize_grammar(features)
      📄 karaka.py
          ⚙️ Functions:
            • infer_karaka(features)
      📄 morphology.py
          🏗️ Classes:
            • class MorphologyAnalyzer:
              - __init__(self, dictionary)
              - analyze_token(self, token)
              - analyze(self, tokens)
      📄 padaccheda.py
          ⚙️ Functions:
            • split_compound(text)
      📄 samasa.py
          ⚙️ Functions:
            • classify_samasa(text)
      📄 tokenizer.py
          🔹 Constants:
            • TOKEN_PATTERN
          ⚙️ Functions:
            • tokenize(text)
    📂 app/
      📄 __init__.py
    📂 application/
      📄 application_service_registry.py
          🏗️ Classes:
            • class ApplicationServiceRegistry:
              - __post_init__(self)
              - engine(self)
              - pipeline(self)
      📄 default_orchestrator.py
          🏗️ Classes:
            • class DefaultOrchestrator:
              - create_context(self, runtime, plan)
              - orchestrate(self, context)
      📄 execution_context.py
          🏗️ Classes:
            • class ExecutionContext:
              - identifier(self)
              - pipeline(self)
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - configuration(self)
              - services(self)
              - plugins(self)
              - resources(self)
              - events(self)
              - __str__(self)
      📄 execution_plan.py
          🏗️ Classes:
            • class ExecutionPlan:
              - identifier(self)
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - stage_count(self)
              - workflow_count(self)
              - step_count(self)
              - task_count(self)
              - __str__(self)
      📄 execution_result.py
          🏗️ Classes:
            • class ExecutionResult:
              - identifier(self)
              - plan(self)
              - pipeline(self)
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - is_success(self)
              - is_failure(self)
              - success_count(self)
              - failure_count(self)
              - has_failures(self)
              - task_count(self)
              - has_results(self)
              - __str__(self)
      📄 execution_strategy.py
          🏗️ Classes:
            • class ExecutionStrategy:
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - execute(self, context)
      📄 orchestrator.py
          🏗️ Classes:
            • class Orchestrator:
              - __init__(self, strategy)
              - strategy(self)
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - create_context(self, runtime, plan)
              - orchestrate(self, context)
      📄 pipeline.py
          🏗️ Classes:
            • class Pipeline:
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - is_empty(self)
              - stage_count(self)
              - workflow_count(self)
              - step_count(self)
              - task_count(self)
              - add_stage(self, stage)
              - __iter__(self)
              - __len__(self)
              - __str__(self)
      📄 pipeline_stage.py
          🏗️ Classes:
            • class PipelineStage:
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - is_empty(self)
              - workflow_count(self)
              - step_count(self)
              - task_count(self)
              - add_workflow(self, workflow)
              - __iter__(self)
              - __len__(self)
              - __str__(self)
      📄 sanskrit_ai.py
          🏗️ Classes:
            • class SanskritAI:
              - from_corpus(cls, corpus)
              - analyze_position(self, position)
              - analyze_sloka(self, position)
              - analyze_word(self, position)
              - navigator(self)
              - knowledge(self)
              - resolution_pipeline(self)
              - search(self, query)
              - ask_ai(self, prompt)
              - generate_commentary(self, position)
      📄 sequential_execution_strategy.py
          🏗️ Classes:
            • class SequentialExecutionStrategy:
              - execute(self, context)
      📄 task.py
          🏗️ Classes:
            • class Task:
              - identifier(self)
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - version(self)
              - capabilities(self)
              - runtime(self)
              - configuration(self)
              - services(self)
              - plugins(self)
              - resources(self)
              - events(self)
              - is_atomic(self)
              - is_interruptible(self)
              - is_retryable(self)
              - __str__(self)
      📄 task_collection.py
          🏗️ Classes:
            • class TaskCollection:
              - identifier(self)
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - is_empty(self)
              - size(self)
              - contains(self, task)
              - add(self, task)
              - remove(self, task)
              - union(self, other)
              - intersection(self, other)
              - difference(self, other)
              - __contains__(self, task)
              - __iter__(self)
              - __len__(self)
              - __str__(self)
      📄 task_metadata.py
          🏗️ Classes:
            • class TaskMetadata:
              - display_description(self)
      📄 task_result.py
          🏗️ Classes:
            • class TaskResult:
              - identifier(self)
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - is_success(self)
              - is_failure(self)
              - has_output(self)
              - has_diagnostics(self)
              - add_diagnostic(self, diagnostic)
              - __str__(self)
      📄 task_result_collection.py
          🏗️ Classes:
            • class TaskResultCollection:
              - identifier(self)
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - is_empty(self)
              - size(self)
              - succeeded(self)
              - failed(self)
              - success_count(self)
              - failure_count(self)
              - all_succeeded(self)
              - any_failed(self)
              - contains(self, result)
              - add(self, result)
              - remove(self, result)
              - union(self, other)
              - intersection(self, other)
              - difference(self, other)
              - __contains__(self, result)
              - __iter__(self)
              - __len__(self)
              - __str__(self)
      📄 work.py
          🏗️ Classes:
            • class Work:
              - identifier(self)
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - version(self)
              - capabilities(self)
              - capability_count(self)
              - supports(self, capability)
              - __str__(self)
      📄 work_context.py
          🏗️ Classes:
            • class WorkContext:
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - configuration(self)
              - services(self)
              - capabilities(self)
              - plugins(self)
              - resources(self)
              - events(self)
              - __str__(self)
      📄 work_metadata.py
          🏗️ Classes:
            • class WorkMetadata:
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - __str__(self)
      📄 workflow.py
          🏗️ Classes:
            • class Workflow:
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - is_empty(self)
              - step_count(self)
              - task_count(self)
              - add_step(self, step)
              - __iter__(self)
              - __len__(self)
              - __str__(self)
      📄 workflow_step.py
          🏗️ Classes:
            • class WorkflowStep:
              - display_name(self)
              - display_text(self)
              - display_description(self)
              - is_empty(self)
              - task_count(self)
              - contains(self, task)
              - __str__(self)
      📂 exceptions/
        📄 acquisition.py
            🏗️ Classes:
              • class AcquisitionException:
              • class DiscoveryException:
              • class RepositoryException:
              • class DownloadException:
              • class ProviderException:
        📄 corpus.py
            🏗️ Classes:
              • class CorpusException:
              • class CorpusValidationException:
              • class DocumentException:
              • class SectionException:
              • class ChapterException:
              • class VerseException:
              • class TokenException:
        📄 parser.py
            🏗️ Classes:
              • class ParserException:
              • class XMLParserException:
              • class HTMLParserException:
              • class TEIParserException:
              • class PDFParserException:
              • class TextParserException:
        📄 registry.py
            🏗️ Classes:
              • class RegistryException:
              • class DuplicateRegistrationException:
              • class RegistrationNotFoundException:
              • class InvalidRegistrationException:
        📄 sanskrit_ai_exception.py
            🏗️ Classes:
              • class SanskritAIException:
                - __init__(self, message)
                - __str__(self)
                - __repr__(self)
                - to_dict(self)
      📂 identifiers/
        📄 base_identifier.py
            🏗️ Classes:
              • class BaseIdentifier:
                - generate(cls)
                - from_string(cls, value)
                - from_uuid(cls, value)
                - to_uuid(self)
                - to_string(self)
                - to_dict(self)
                - __str__(self)
                - __repr__(self)
        📄 chapter_id.py
            🏗️ Classes:
              • class ChapterId:
        📄 corpus_id.py
            🏗️ Classes:
              • class CorpusId:
        📄 document_id.py
            🏗️ Classes:
              • class DocumentId:
        📄 line_id.py
            🏗️ Classes:
              • class LineId:
        📄 paragraph_id.py
            🏗️ Classes:
              • class ParagraphId:
        📄 section_id.py
            🏗️ Classes:
              • class SectionId:
        📄 token_id.py
            🏗️ Classes:
              • class TokenId:
        📄 verse_id.py
            🏗️ Classes:
              • class VerseId:
      📂 metadata/
        📄 confidence_score.py
            🏗️ Classes:
              • class ConfidenceScore:
                - __post_init__(self)
                - percentage(self)
                - is_high(self, threshold)
                - is_low(self, threshold)
                - to_dict(self)
                - __str__(self)
        📄 provenance.py
            🏗️ Classes:
              • class Provenance:
                - add_note(self, note)
                - to_dict(self)
        📄 source_reference.py
            🏗️ Classes:
              • class SourceReference:
                - is_remote(self)
                - is_local(self)
                - to_dict(self)
    📂 core/
      📄 __init__.py
      📄 config.py
          🔹 Constants:
            • LEXICAL_REPOSITORY
      📄 config_backup.py
          🔹 Constants:
            • PROJECT_ROOT
            • DATA_DIR
            • OUTPUT_DIR
            • DEFAULT_DICTIONARY
      📄 constants.py
          🔹 Constants:
            • DANDA
            • DOUBLE_DANDA
            • SANSKRIT_PUNCTUATION
      📄 exceptions.py
          🏗️ Classes:
            • class SanskritAIError:
            • class DictionaryFormatError:
      📄 typing.py
          🔹 Constants:
            • T
            • KT
            • VT
      📄 version.py
          ⚙️ Functions:
            • get_version()
      📂 builders/
        📄 build_result.py
            🏗️ Classes:
              • class BuildResult:
                - is_success(self)
                - has_object(self)
                - has_errors(self)
                - success(cls, obj)
                - failure(cls, validation)
        📄 record_builder.py
            🏗️ Classes:
              • class RecordBuilder:
                - record_type(self)
        📄 validated_builder.py
            🏗️ Classes:
              • class ValidatedBuilder:
                - __init__(self, validator)
                - validate(self, record)
                - build(self, record)
                - build_validated(self, record)
                - build_many(self, records)
      📂 capabilities/
        📄 __init__.py
        📄 capability.py
            🏗️ Classes:
              • class Capability:
                - __post_init__(self)
                - identifier(self)
                - display_name(self)
                - display_description(self)
                - matches(self, name)
                - __str__(self)
        📄 capability_profile.py
            🏗️ Classes:
              • class CapabilityProfile:
                - __post_init__(self)
                - identifier(self)
                - supports(self, capability)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
        📄 capability_provider.py
            🏗️ Classes:
              • class CapabilityProvider:
                - capability_profile(self)
                - capabilities(self)
                - supports(self, capability)
        📄 capability_registry.py
            🏗️ Classes:
              • class CapabilityRegistry:
                - count(self)
                - register(self, capability)
                - unregister(self, capability)
                - contains(self, capability)
                - lookup(self, name)
                - display_name(self)
                - display_text(self)
                - __contains__(self, capability)
                - __len__(self)
                - __iter__(self)
                - __bool__(self)
                - __str__(self)
        📄 capability_set.py
            🏗️ Classes:
              • class CapabilitySet:
                - count(self)
                - is_empty(self)
                - contains(self, capability)
                - add(self, capability)
                - remove(self, capability)
                - union(self, other)
                - intersection(self, other)
                - difference(self, other)
                - is_subset_of(self, other)
                - is_superset_of(self, other)
                - display_name(self)
                - display_text(self)
                - __contains__(self, capability)
                - __len__(self)
                - __iter__(self)
                - __bool__(self)
                - __str__(self)
      📂 collections/
        📄 node_collection.py
            🏗️ Classes:
              • class NodeCollection:
                - __init__(self, items)
                - add(self, item)
                - extend(self, items)
                - remove(self, item)
                - clear(self)
                - first(self)
                - last(self)
                - to_list(self)
                - __iter__(self)
                - __getitem__(self, index)
                - __contains__(self, item)
                - __len__(self)
                - __bool__(self)
                - __eq__(self, other)
                - __repr__(self)
      📂 configuration/
        📄 __init__.py
        📄 configuration.py
            🏗️ Classes:
              • class Configuration:
                - count(self)
                - is_empty(self)
                - contains(self, key)
                - lookup(self, key)
                - add(self, entry)
                - remove(self, key)
                - display_name(self)
                - display_text(self)
                - __contains__(self, key)
                - __len__(self)
                - __iter__(self)
                - __bool__(self)
                - __str__(self)
        📄 configuration_context.py
            🏗️ Classes:
              • class ConfigurationContext:
                - identifier(self)
                - configuration(self)
                - contains(self, key)
                - lookup(self, key)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
        📄 configuration_entry.py
            🏗️ Classes:
              • class ConfigurationEntry:
                - identifier(self)
                - has_default(self)
                - default_value(self)
                - is_required(self)
                - is_read_only(self)
                - is_deprecated(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - with_value(self, value)
                - enable(self)
                - disable(self)
                - __str__(self)
        📄 configuration_key.py
            🏗️ Classes:
              • class ConfigurationKey:
                - __post_init__(self)
                - identifier(self)
                - segments(self)
                - parent(self)
                - leaf(self)
                - display_name(self)
                - display_text(self)
                - starts_with(self, prefix)
                - __str__(self)
        📄 configuration_metadata.py
            🏗️ Classes:
              • class ConfigurationMetadata:
                - has_default(self)
                - is_mutable(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
        📄 configuration_profile.py
            🏗️ Classes:
              • class ConfigurationProfile:
                - __post_init__(self)
                - identifier(self)
                - count(self)
                - contains(self, key)
                - lookup(self, key)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
        📄 configuration_provider.py
            🏗️ Classes:
              • class ConfigurationProvider:
                - configuration_context(self)
                - configuration(self)
                - contains(self, key)
                - lookup(self, key)
        📄 configuration_registry.py
            🏗️ Classes:
              • class ConfigurationRegistry:
                - count(self)
                - is_empty(self)
                - register(self, profile)
                - unregister(self, identifier)
                - lookup(self, identifier)
                - contains(self, identifier)
                - display_name(self)
                - display_text(self)
                - __contains__(self, identifier)
                - __len__(self)
                - __iter__(self)
                - __bool__(self)
                - __str__(self)
        📄 configuration_source.py
            🏗️ Classes:
              • class ConfigurationSource:
                - __post_init__(self)
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - matches(self, name)
                - __str__(self)
        📄 configuration_value.py
            🔹 Constants:
              • T
            🏗️ Classes:
              • class ConfigurationValue:
                - type(self)
                - type_name(self)
                - is_none(self)
                - is_scalar(self)
                - is_collection(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_instance_of(self, expected_type)
                - unwrap(self)
                - __str__(self)
      📂 contracts/
        📄 __init__.py
        📄 buildable.py
            🏗️ Classes:
              • class Buildable:
                - can_build(self)
                - builder_type(self)
                - record_type(self)
        📄 contract.py
            🏗️ Classes:
              • class Contract:
                - contract_name(self)
                - contract_module(self)
                - contract_qualified_name(self)
                - is_contract(self)
                - __repr__(self)
        📄 identifiable.py
            🏗️ Classes:
              • class Identifiable:
                - identifier(self)
                - has_identifier(self)
                - same_identity_as(self, other)
        📄 parsable.py
            🏗️ Classes:
              • class Parsable:
                - parse(self, source)
        📄 processable.py
            🏗️ Classes:
              • class Processable:
                - process(self, *args, **kwargs)
                - can_process(self)
                - processor_name(self)
                - processor_type(self)
        📄 searchable.py
            🏗️ Classes:
              • class Searchable:
                - search(self, query)
                - contains(self, query)
        📄 serializable.py
            🏗️ Classes:
              • class Serializable:
                - serialize(self, format)
        📄 tokenizable.py
            🏗️ Classes:
              • class Tokenizable:
                - tokenize(self, source)
        📄 validatable.py
            🏗️ Classes:
              • class Validatable:
                - validate(self)
                - is_valid(self)
                - can_validate(self)
      📂 dependency/
        📄 service_collection.py
            🏗️ Classes:
              • class ServiceCollection:
                - count(self)
                - is_empty(self)
                - contains(self, key)
                - lookup(self, key)
                - add(self, descriptor)
                - remove(self, key)
                - display_name(self)
                - display_text(self)
                - __contains__(self, key)
                - __len__(self)
                - __iter__(self)
                - __bool__(self)
                - __str__(self)
        📄 service_container.py
            🏗️ Classes:
              • class ServiceContainer:
                - identifier(self)
                - service_count(self)
                - is_empty(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __len__(self)
                - __bool__(self)
                - __str__(self)
        📄 service_descriptor.py
            🏗️ Classes:
              • class ServiceDescriptor:
                - identifier(self)
                - service_type(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_singleton(self)
                - is_scoped(self)
                - is_transient(self)
                - create(self, *args, **kwargs)
                - __str__(self)
        📄 service_factory.py
            🏗️ Classes:
              • class ServiceFactory:
                - __post_init__(self)
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - create(self, *args, **kwargs)
                - __call__(self, *args, **kwargs)
                - __str__(self)
        📄 service_key.py
            🏗️ Classes:
              • class ServiceKey:
                - __post_init__(self)
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - matches(self, service_type, name)
                - __str__(self)
        📄 service_lifetime.py
            🏗️ Classes:
              • class ServiceLifetime:
                - __post_init__(self)
                - identifier(self)
                - is_singleton(self)
                - is_scoped(self)
                - is_transient(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
        📄 service_provider.py
            🏗️ Classes:
              • class ServiceProvider:
                - identifier(self)
                - contains(self, key)
                - get_descriptor(self, key)
                - get_service(self, key, **kwargs)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
        📄 service_resolver.py
            🏗️ Classes:
              • class ServiceResolver:
                - services(self)
                - resolve(self, key)
                - try_resolve(self, key)
                - contains(self, key)
        📄 service_scope.py
            🏗️ Classes:
              • class ServiceScope:
                - __post_init__(self)
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - matches(self, name)
                - __str__(self)
        📄 service_type.py
            🏗️ Classes:
              • class ServiceType:
                - __post_init__(self)
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - matches(self, name)
                - __str__(self)
      📂 diagnostics/
        📄 __init__.py
        📄 diagnostic.py
            🏗️ Classes:
              • class Diagnostic:
                - is_error(self)
                - is_warning(self)
                - is_information(self)
                - is_fatal(self)
                - has_location(self)
                - has_metadata(self)
                - __str__(self)
                - __repr__(self)
        📄 diagnostic_code.py
            🏗️ Classes:
              • class DiagnosticCode:
                - __post_init__(self)
                - subsystem(self)
                - number(self)
                - is_tokenizer(self)
                - is_parser(self)
                - is_morphology(self)
                - __str__(self)
                - __repr__(self)
        📄 diagnostic_collection.py
            🏗️ Classes:
              • class DiagnosticCollection:
                - size(self)
                - is_empty(self)
                - has_errors(self)
                - has_warnings(self)
                - has_information(self)
                - has_fatal(self)
                - count(self, severity)
                - filter(self, severity)
                - __len__(self)
                - __iter__(self)
                - __getitem__(self, index)
                - __contains__(self, diagnostic)
                - __str__(self)
                - __repr__(self)
        📄 diagnostic_report.py
            🏗️ Classes:
              • class DiagnosticReport:
                - total(self)
                - errors(self)
                - warnings(self)
                - infos(self)
                - fatals(self)
                - has_errors(self)
                - has_warnings(self)
                - has_fatal(self)
                - is_clean(self)
                - is_successful(self)
                - __bool__(self)
                - __str__(self)
                - __repr__(self)
        📄 diagnostic_severity.py
            🏗️ Classes:
              • class DiagnosticSeverity:
                - is_error(self)
                - is_warning(self)
                - is_information(self)
                - is_fatal(self)
                - priority(self)
      📂 events/
        📄 event.py
            🏗️ Classes:
              • class Event:
                - identifier(self)
                - event_identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - name(self)
                - event_type(self)
                - priority(self)
                - to_dict(self)
                - __repr__(self)
                - __str__(self)
        📄 event_dispatcher.py
            🏗️ Classes:
              • class EventDispatcher:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - dispatch(self, event)
                - __call__(self, event)
                - __str__(self)
        📄 event_handler.py
            🏗️ Classes:
              • class EventHandler:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __call__(self, event)
                - __str__(self)
        📄 event_id.py
            🏗️ Classes:
              • class EventId:
                - __post_init__(self)
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - matches(self, identifier)
                - __str__(self)
        📄 event_metadata.py
            🏗️ Classes:
              • class EventMetadata:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_critical(self)
                - __str__(self)
        📄 event_priority.py
            🏗️ Classes:
              • class EventPriority:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
        📄 event_registry.py
            🏗️ Classes:
              • class EventRegistry:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - subscriptions_for(self, event)
                - contains(self, identifier)
                - __len__(self)
                - __iter__(self)
                - __str__(self)
        📄 event_subscription.py
            🏗️ Classes:
              • class EventSubscription:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - supports(self, event)
                - invoke(self, event)
                - __str__(self)
        📄 event_type.py
            🏗️ Classes:
              • class EventType:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
      📂 factories/
        📄 object_factory.py
            🔹 Constants:
              • T
            🏗️ Classes:
              • class ObjectFactory:
                - register(cls, object_type, constructor)
                - unregister(cls, object_type)
                - create(cls, object_type, *args, **kwargs)
                - is_registered(cls, object_type)
                - registered_types(cls)
                - clear(cls)
                - constructor_for(cls, object_type)
      📂 identities/
        📄 __init__.py
        📄 corpus_identifier.py
            🏗️ Classes:
              • class CorpusIdentifier:
                - __post_init__(self)
                - corpus_name(self)
                - corpus_path(self)
                - location(self)
                - location_depth(self)
                - root_resource(self)
                - __repr__(self)
        📄 hierarchical_identifier.py
            🏗️ Classes:
              • class HierarchicalIdentifier:
                - __post_init__(self)
                - depth(self)
                - root(self)
                - leaf(self)
                - parent(self)
                - child(self, component)
                - starts_with(self, other)
                - __str__(self)
        📄 identifier.py
            🏗️ Classes:
              • class Identifier:
                - __post_init__(self)
                - is_empty(self)
                - length(self)
                - starts_with(self, prefix)
                - ends_with(self, suffix)
                - __str__(self)
                - __repr__(self)
        📄 knowledge_identifier.py
            🏗️ Classes:
              • class KnowledgeIdentifier:
                - __post_init__(self)
                - knowledge_source(self)
                - concept_path(self)
                - concept_name(self)
                - concept_depth(self)
                - concept_location(self)
                - __repr__(self)
        📄 lexical_identifier.py
            🏗️ Classes:
              • class LexicalIdentifier:
                - __post_init__(self)
                - lemma(self)
                - lexical_path(self)
                - sense_number(self)
                - __repr__(self)
        📄 namespaced_identifier.py
            🏗️ Classes:
              • class NamespacedIdentifier:
                - __post_init__(self)
                - local_identifier(self)
                - has_multiple_levels(self)
                - with_local(self, *components)
                - __str__(self)
        📄 resource_identifier.py
            🏗️ Classes:
              • class ResourceIdentifier:
                - resource_name(self)
                - resource_path(self)
                - resource_depth(self)
                - parent_resource(self)
                - child_resource(self, component)
                - is_descendant_of(self, other)
                - __repr__(self)
        📄 uuid_identifier.py
            🏗️ Classes:
              • class UUIDIdentifier:
                - __post_init__(self)
                - uuid(self)
                - hex(self)
                - version(self)
                - generate(cls, namespace)
                - from_uuid(cls, namespace, value)
                - __str__(self)
      📂 indexing/
        📄 immutable_index.py
            🔹 Constants:
              • K
              • V
            🏗️ Classes:
              • class ImmutableIndex:
                - build(cls, items)
                - get(self, key)
                - first(self, key)
                - contains(self, key)
                - keys(self)
                - values(self)
                - item_count(self)
                - key_count(self)
                - __contains__(self, key)
                - __len__(self)
                - __iter__(self)
                - summary(self)
                - __str__(self)
        📄 indexed_collection.py
            🔹 Constants:
              • T
            🏗️ Classes:
              • class IndexedCollection:
                - count(self)
                - is_empty(self)
                - contains(self, item)
                - __contains__(self, item)
                - __len__(self)
                - __iter__(self)
                - summary(self)
                - __str__(self)
        📄 multi_index.py
            🏗️ Classes:
              • class MultiIndex:
                - get_index(self, name)
                - contains_index(self, name)
                - names(self)
                - count(self)
                - __contains__(self, name)
                - __len__(self)
                - __iter__(self)
                - summary(self)
                - __str__(self)
      📂 infrastructure/
        📄 component.py
            🏗️ Classes:
              • class Component:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - lifecycle(self)
                - is_active(self)
                - is_terminal(self)
                - __str__(self)
        📄 component_metadata.py
            🏗️ Classes:
              • class ComponentMetadata:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_active(self)
                - is_terminal(self)
                - __str__(self)
        📄 event_bus.py
            🏗️ Classes:
              • class EventBus:
                - __init__(self)
                - subscribe(self, event_type, handler)
                - unsubscribe(self, event_type, handler)
                - publish(self, envelope)
                - subscribed_event_types(self)
                - clear(self)
                - __len__(self)
                - __repr__(self)
        📄 event_channel.py
            🏗️ Classes:
              • class EventChannel:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - publish(self, envelope)
                - __str__(self)
        📄 event_envelope.py
            🏗️ Classes:
              • class EventEnvelope:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - event_identifier(self)
                - event_instance_id(self)
                - event_type(self)
                - priority(self)
                - with_header(self, key, value)
                - __str__(self)
        📄 event_publisher.py
            🏗️ Classes:
              • class EventPublisher:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - publish(self, envelope)
                - __call__(self, envelope)
                - __str__(self)
        📄 event_subscriber.py
            🏗️ Classes:
              • class EventSubscriber:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - subscribe(self, event_type, handler)
                - unsubscribe(self, event_type, handler)
                - __str__(self)
        📄 infrastructure_service.py
            🏗️ Classes:
              • class InfrastructureService:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - lifecycle(self)
                - is_active(self)
                - is_terminal(self)
                - with_lifecycle(self, lifecycle)
                - __str__(self)
        📄 lifecycle.py
            🏗️ Classes:
              • class Lifecycle:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_active(self)
                - is_terminal(self)
                - transition_to(self, state)
                - __str__(self)
        📄 lifecycle_manager.py
            🏗️ Classes:
              • class LifecycleManager:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - transition(self, service, state)
                - __str__(self)
        📄 runtime_context.py
            🏗️ Classes:
              • class RuntimeContext:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
        📄 runtime_environment.py
            🏗️ Classes:
              • class RuntimeEnvironment:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_running(self)
                - is_terminal(self)
                - transition_to(self, state)
                - __str__(self)
        📄 runtime_state.py
            🏗️ Classes:
              • class RuntimeState:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_active(self)
                - is_terminal(self)
                - __str__(self)
      📂 interfaces/
        📄 __init__.py
        📄 builder.py
            🏗️ Classes:
              • class Builder:
                - reset(self)
                - build(self)
                - validate(self)
                - from_instance(self, instance)
                - instance(self)
        📄 hierarchical.py
            🏗️ Classes:
              • class Hierarchical:
                - children(self)
                - add_child(self, child)
                - remove_child(self, child)
                - child_count(self)
                - is_leaf(self)
        📄 identifiable.py
            🏗️ Classes:
              • class Identifiable:
                - id(self)
                - identifier(self)
                - has_identifier(self)
        📄 repository.py
            🏗️ Classes:
              • class Repository:
                - add(self, obj)
                - remove(self, identifier)
                - get(self, identifier)
                - exists(self, identifier)
                - all(self)
                - clear(self)
                - __contains__(self, identifier)
                - __iter__(self)
                - __len__(self)
        📄 serializable.py
            🏗️ Classes:
              • class Serializable:
                - to_dict(self)
                - from_dict(cls, data)
                - copy_dict(self)
      📂 location/
        📄 __init__.py
        📄 location.py
            🏗️ Classes:
              • class Location:
                - __post_init__(self)
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
        📄 location_kind.py
            🏗️ Classes:
              • class LocationKind:
                - identifier(self)
                - display_name(self)
                - __str__(self)
        📄 path.py
            🏗️ Classes:
              • class Path:
                - __init__(self, value)
        📄 uri.py
            🏗️ Classes:
              • class URI:
                - __init__(self, value)
      📂 mixins/
        📄 displayable.py
            🏗️ Classes:
              • class Displayable:
                - is_displayable(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - to_display_string(self)
        📄 immutable.py
            🏗️ Classes:
              • class Immutable:
                - is_immutable(self)
                - field_count(self)
                - field_names(self)
                - as_dict(self)
                - copy(self, **changes)
        📄 repr_mixin.py
            🏗️ Classes:
              • class ReprMixin:
                - __repr__(self)
        📄 serialization_mixin.py
            🏗️ Classes:
              • class SerializationMixin:
                - to_dict(self)
                - copy_dict(self)
      📂 parsers/
        📄 base_parser.py
            🏗️ Classes:
              • class BaseParser:
                - __init__(self)
                - name(self)
                - version(self)
                - normalize_source(self, source)
                - parse_many(self, source)
                - supports(self, source)
                - parse(self, source)
        📄 parser.py
            🏗️ Classes:
              • class Parser:
                - parse(self, source)
                - parse_many(self, source)
                - supports(self, source)
        📂 cursor/
          📄 __init__.py
          📄 cursor_exception.py
              🏗️ Classes:
                • class CursorException:
                  - __str__(self)
                  - __repr__(self)
          📄 cursor_mark.py
              🏗️ Classes:
                • class CursorMark:
                  - is_named(self)
                  - __str__(self)
          📄 cursor_state.py
              🏗️ Classes:
                • class CursorState:
                  - is_valid(self)
                  - can_advance(self)
                  - is_terminal(self)
                  - advance(self, step)
                  - with_eof(self)
                  - with_error(self)
                  - reset(self)
                  - __str__(self)
          📄 parser_cursor.py
              🏗️ Classes:
                • class ParserCursor:
                  - __init__(self, stream)
                  - stream(self)
                  - state(self)
                  - index(self)
                  - eof(self)
                  - current(self)
                  - peek(self, offset)
                  - previous(self)
                  - advance(self, count)
                  - consume(self)
                  - mark(self, label)
                  - restore(self, mark)
                  - reset(self)
                  - remaining(self)
                  - __iter__(self)
                  - __len__(self)
                  - __repr__(self)
      📂 pipeline/
        📄 pipeline.py
            🏗️ Classes:
              • class Pipeline:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - ordered_steps(self)
                - step_count(self)
                - is_empty(self)
                - add_step(self, step)
                - before_execute(self, context)
                - after_execute(self, context, result)
                - execute(self, context)
                - __call__(self, context)
                - __str__(self)
        📄 pipeline_builder.py
            🏗️ Classes:
              • class PipelineBuilder:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - named(self, name)
                - add_step(self, step)
                - add_steps(self, *steps)
                - clear(self)
                - step_count(self)
                - is_empty(self)
                - ordered_steps(self)
                - build(self)
                - __len__(self)
                - __str__(self)
        📄 pipeline_context.py
            🏗️ Classes:
              • class PipelineContext:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_subject(self)
                - has_metadata(self)
                - metadata_count(self)
                - get(self, key, default)
                - has(self, key)
                - __str__(self)
        📄 pipeline_factory.py
            🏗️ Classes:
              • class PipelineFactory:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - register(self, pipeline)
                - get(self, name)
                - require(self, name)
                - create(self, name)
                - create_from_builder(self, builder)
                - pipeline_count(self)
                - pipelines(self)
                - names(self)
                - __contains__(self, name)
                - __len__(self)
                - __iter__(self)
                - __str__(self)
        📄 pipeline_registry.py
            🏗️ Classes:
              • class PipelineRegistry:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - register(self, pipeline)
                - unregister(self, name)
                - clear(self)
                - get(self, name)
                - require(self, name)
                - contains(self, name)
                - pipelines(self)
                - names(self)
                - pipeline_count(self)
                - is_empty(self)
                - is_not_empty(self)
                - __iter__(self)
                - __len__(self)
                - __contains__(self, name)
                - __str__(self)
        📄 pipeline_result.py
            🏗️ Classes:
              • class PipelineResult:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - subject(self)
                - metadata(self)
                - source(self)
                - language(self)
                - script(self)
                - has_output(self)
                - result(self)
                - resolved(self)
                - unresolved(self)
                - is_confident(self)
                - is_uncertain(self)
                - has_trace(self)
                - step_count(self)
                - successful_steps(self)
                - failed_steps(self)
                - first_step(self)
                - last_step(self)
                - has_diagnostics(self)
                - diagnostic_count(self)
                - first_diagnostic(self)
                - __str__(self)
        📄 pipeline_step.py
            🏗️ Classes:
              • class PipelineStep:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - execute(self, context, previous_result)
                - is_enabled(self)
                - is_disabled(self)
                - __lt__(self, other)
                - __str__(self)
        📄 pipeline_trace.py
            🏗️ Classes:
              • class PipelineTraceEntry:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_output(self)
                - has_input(self)
                - has_diagnostics(self)
                - diagnostic_count(self)
                - __str__(self)
              • class PipelineTrace:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - first(self)
                - last(self)
                - is_empty(self)
                - is_not_empty(self)
                - successful_steps(self)
                - failed_steps(self)
                - success_count(self)
                - failure_count(self)
                - succeeded(self)
                - add(self, entry)
                - __str__(self)
        📄 universal_kernel_pipeline.py
            🏗️ Classes:
              • class UniversalKernelPipeline:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - pipeline_count(self)
                - kernel_names(self)
                - is_empty(self)
                - is_not_empty(self)
                - execute(self, context)
                - execute_with_trace(self, context)
                - append(self, pipeline)
                - __iter__(self)
                - __len__(self)
                - __str__(self)
      📂 plugins/
        📄 plugin_capability.py
            🏗️ Classes:
              • class PluginCapability:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
        📄 plugin_dependency.py
            🏗️ Classes:
              • class PluginDependency:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_required(self)
                - __str__(self)
        📄 plugin_descriptor.py
            🏗️ Classes:
              • class PluginDescriptor:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
        📄 plugin_id.py
            🏗️ Classes:
              • class PluginId:
                - __post_init__(self)
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - matches(self, identifier)
                - __str__(self)
        📄 plugin_loader.py
            🏗️ Classes:
              • class PluginLoader:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - contains(self, identifier)
                - descriptor(self, identifier)
                - validate(self)
                - planned_plugins(self)
                - __str__(self)
        📄 plugin_manifest.py
            🏗️ Classes:
              • class PluginManifest:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_implementation(self)
                - __str__(self)
        📄 plugin_metadata.py
            🏗️ Classes:
              • class PluginMetadata:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - dependency_count(self)
                - capability_count(self)
                - __str__(self)
        📄 plugin_registry.py
            🏗️ Classes:
              • class PluginRegistry:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - contains(self, identifier)
                - lookup(self, identifier)
                - __len__(self)
                - __bool__(self)
                - __str__(self)
        📄 plugin_state.py
            🏗️ Classes:
              • class PluginState:
                - identifier(self)
                - display_name(self)
                - is_active(self)
                - is_terminal(self)
                - __str__(self)
      📂 protocols/
        📄 __init__.py
        📄 categories.py
            🏗️ Classes:
              • class ProtocolCategory:
        📄 protocol.py
            🏗️ Classes:
              • class Protocol:
        📄 supports_collection.py
            🔹 Constants:
              • T
            🏗️ Classes:
              • class SupportsCollection:
                - __len__(self)
                - __contains__(self, item)
        📄 supports_iteration.py
            🔹 Constants:
              • T
            🏗️ Classes:
              • class SupportsIteration:
                - __iter__(self)
        📄 supports_lookup.py
            🔹 Constants:
              • K
              • V
            🏗️ Classes:
              • class SupportsLookup:
                - lookup(self, key, default)
                - __contains__(self, key)
                - __getitem__(self, key)
        📄 supports_processing.py
            🔹 Constants:
              • I
              • R
            🏗️ Classes:
              • class SupportsProcessing:
                - process(self, value)
        📄 supports_registry.py
            🔹 Constants:
              • K
              • V
            🏗️ Classes:
              • class SupportsRegistry:
                - register(self, key, value)
                - unregister(self, key)
                - lookup(self, key, default)
                - __contains__(self, key)
                - __len__(self)
                - __iter__(self)
        📄 supports_search.py
            🔹 Constants:
              • Q
              • R
            🏗️ Classes:
              • class SupportsSearch:
                - search(self, query)
        📄 supports_serialization.py
            🔹 Constants:
              • F
              • R
            🏗️ Classes:
              • class SupportsSerialization:
                - serialize(self, format)
      📂 records/
        📄 __init__.py
        📄 corpus_record.py
            🏗️ Classes:
              • class CorpusRecord:
        📄 data_record.py
            🏗️ Classes:
              • class DataRecord:
                - has_source(self)
                - is_active(self)
        📄 knowledge_record.py
            🏗️ Classes:
              • class KnowledgeRecord:
        📄 lexical_record.py
            🏗️ Classes:
              • class LexicalRecord:
      📂 registries/
        📄 base_registry.py
            🏗️ Classes:
              • class BaseRegistry:
                - __init__(self)
                - add(self, obj)
                - remove(self, identifier)
                - get(self, identifier)
                - exists(self, identifier)
                - all(self)
                - clear(self)
                - identifiers(self)
                - values(self)
                - items(self)
                - __iter__(self)
                - __len__(self)
                - __repr__(self)
      📂 registry/
        📄 __init__.py
        📄 base_registry.py
            🔹 Constants:
              • T
            🏗️ Classes:
              • class BaseRegistry:
                - __init__(self, registry_path)
                - collection_name(self)
                - create_item(self, data)
                - get_identifier(self, item)
                - items(self)
                - _load_json(self)
                - _validate_registry(self, data)
                - get(self, identifier)
                - exists(self, identifier)
                - identifiers(self)
                - all(self)
                - reload(self)
                - __iter__(self)
                - __len__(self)
                - __contains__(self, identifier)
                - __getitem__(self, identifier)
                - registry_path(self)
                - __repr__(self)
        📄 hierarchical_registry.py
            🔹 Constants:
              • K
              • V
            🏗️ Classes:
              • class HierarchicalRegistry:
                - __init__(self, value_type)
                - add_node(self, node)
                - get_node(self, key)
                - contains_node(self, key)
                - parent_of(self, key)
                - children_of(self, key)
                - path_of(self, key)
                - root_nodes(self)
                - all_nodes(self)
                - node_count(self)
        📄 immutable_registry.py
            🔹 Constants:
              • K
              • V
            🏗️ Classes:
              • class ImmutableRegistry:
                - __init__(self, value_type, entries)
                - register(self, key, value)
                - unregister(self, key)
                - clear(self)
                - is_mutable(self)
                - is_immutable(self)
        📄 mutable_registry.py
            🔹 Constants:
              • K
              • V
            🏗️ Classes:
              • class MutableRegistry:
                - __init__(self)
                - register(self, key, value)
                - unregister(self, key)
                - contains(self, key)
                - get(self, key)
                - get_entry(self, key)
                - keys(self)
                - values(self)
                - items(self)
                - entries(self)
                - clear(self)
                - size(self)
        📄 ordered_registry.py
            🔹 Constants:
              • K
              • V
            🏗️ Classes:
              • class OrderedRegistry:
                - __init__(self, value_type)
                - is_ordered(self)
                - first(self)
                - last(self)
                - entries(self)
                - reversed_entries(self)
        📄 registry.py
            🔹 Constants:
              • K
              • V
            🏗️ Classes:
              • class Registry:
                - register(self, key, value)
                - unregister(self, key)
                - contains(self, key)
                - get(self, key)
                - keys(self)
                - values(self)
                - items(self)
                - clear(self)
                - size(self)
                - is_empty(self)
                - __len__(self)
                - __contains__(self, key)
        📄 registry_entry.py
            🏗️ Classes:
              • class RegistryEntry:
                - __post_init__(self)
                - is_enabled(self)
                - has_metadata(self)
                - __str__(self)
        📄 registry_exception.py
            🏗️ Classes:
              • class RegistryException:
                - __init__(self, message)
                - message(self)
                - key(self)
                - value(self)
                - cause(self)
                - has_cause(self)
                - __str__(self)
        📄 registry_key.py
            🏗️ Classes:
              • class RegistryKey:
                - __post_init__(self)
                - __str__(self)
        📄 registry_node.py
            🏗️ Classes:
              • class RegistryNode:
                - is_root(self)
                - is_leaf(self)
                - child_count(self)
                - has_child(self, key)
                - __str__(self)
        📄 registry_path.py
            🏗️ Classes:
              • class RegistryPath:
                - __post_init__(self)
                - is_root(self)
                - depth(self)
                - parent(self)
                - leaf(self)
                - append(self, key)
                - starts_with(self, other)
                - __iter__(self)
                - __len__(self)
                - __str__(self)
        📄 registry_result.py
            🏗️ Classes:
              • class RegistryResult:
                - is_success(self)
                - is_failure(self)
                - is_informational(self)
                - has_entry(self)
                - has_exception(self)
                - success(cls, status)
                - failure(cls, status)
                - __bool__(self)
        📄 registry_status.py
            🏗️ Classes:
              • class RegistryStatus:
                - is_success(self)
                - is_failure(self)
                - is_informational(self)
        📄 typed_registry.py
            🔹 Constants:
              • K
              • V
            🏗️ Classes:
              • class TypedRegistry:
                - __init__(self, value_type)
                - value_type(self)
                - register(self, key, value)
                - accepts(self, value)
      📂 resources/
        📄 resource_descriptor.py
            🏗️ Classes:
              • class ResourceDescriptor:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
        📄 resource_id.py
            🏗️ Classes:
              • class ResourceId:
                - __post_init__(self)
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - matches(self, identifier)
                - __str__(self)
        📄 resource_locator.py
            🏗️ Classes:
              • class ResourceLocator:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - locate(self, identifier)
        📄 resource_manifest.py
            🏗️ Classes:
              • class ResourceManifest:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
        📄 resource_metadata.py
            🏗️ Classes:
              • class ResourceMetadata:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
        📄 resource_registry.py
            🏗️ Classes:
              • class ResourceRegistry:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - lookup(self, identifier)
        📄 resource_state.py
            🏗️ Classes:
              • class ResourceState:
                - identifier(self)
                - display_name(self)
                - __str__(self)
        📄 resource_type.py
            🏗️ Classes:
              • class ResourceType:
                - identifier(self)
                - display_name(self)
                - __str__(self)
      📂 search/
        📄 __init__.py
        📄 search_language.py
            🏗️ Classes:
              • class SearchLanguage:
                - is_policy(self)
                - is_indic(self)
                - is_single_language(self)
        📄 search_match.py
            🏗️ Classes:
              • class SearchMatch:
                - __post_init__(self)
                - has_score(self)
                - has_rank(self)
                - has_location(self)
                - has_metadata(self)
                - metadata_value(self, key, default)
                - __str__(self)
        📄 search_mode.py
            🏗️ Classes:
              • class SearchMode:
                - is_lexical(self)
                - is_semantic(self)
                - is_ai_ready(self)
        📄 search_operator.py
            🏗️ Classes:
              • class SearchOperator:
                - is_boolean(self)
                - is_structural(self)
        📄 search_options.py
            🏗️ Classes:
              • class SearchOptions:
                - is_paged(self)
                - is_exact(self)
                - is_semantic(self)
        📄 search_order.py
            🏗️ Classes:
              • class SearchOrder:
                - is_alphabetical(self)
                - is_ai_ranking(self)
                - is_relevance_based(self)
        📄 search_query.py
            🏗️ Classes:
              • class SearchQuery:
                - __post_init__(self)
                - term_count(self)
                - is_single_term(self)
                - is_multi_term(self)
                - append(self, term)
                - __iter__(self)
                - __len__(self)
                - __str__(self)
        📄 search_result.py
            🏗️ Classes:
              • class SearchResult:
                - __post_init__(self)
                - count(self)
                - is_empty(self)
                - has_matches(self)
                - best_match(self)
                - effective_total(self)
                - metadata_value(self, key, default)
                - __len__(self)
                - __iter__(self)
                - __getitem__(self, index)
                - __bool__(self)
                - __str__(self)
        📄 search_scope.py
            🏗️ Classes:
              • class SearchScope:
                - is_ai_scope(self)
                - is_linguistic(self)
        📄 search_term.py
            🏗️ Classes:
              • class SearchTerm:
                - __post_init__(self)
                - is_phrase(self)
                - is_negated(self)
                - is_boosted(self)
                - normalized(self)
                - __str__(self)
      📂 serialization/
        📄 __init__.py
        📄 serializable.py
            🏗️ Classes:
              • class Serializable:
                - to_dict(self)
                - from_dict(cls, data)
                - is_serializable(self)
        📄 serialization_format.py
            🏗️ Classes:
              • class SerializationFormat:
                - is_text(self)
                - is_binary(self)
                - is_native(self)
                - extension(self)
        📄 serialization_result.py
            🏗️ Classes:
              • class SerializationResult:
                - has_data(self)
                - has_diagnostics(self)
                - is_successful(self)
                - is_empty(self)
                - __bool__(self)
                - __str__(self)
                - __repr__(self)
        📄 serializer.py
            🔹 Constants:
              • S
              • R
            🏗️ Classes:
              • class Serializer:
                - serialize(self, obj)
                - deserialize(self, data, object_type)
                - can_serialize(self, obj)
                - name(self)
      📂 tokenizers/
        📄 __init__.py
        📄 base_tokenizer.py
            🏗️ Classes:
              • class BaseTokenizer:
                - __init__(self)
                - name(self)
                - version(self)
                - normalize_source(self, source)
                - preprocess(self, source)
                - postprocess(self, result)
                - tokenize_many(self, sources)
                - supports(self, source)
                - tokenize(self, source)
        📄 token_position.py
            🏗️ Classes:
              • class TokenPosition:
                - length(self)
                - is_valid(self)
                - shift(self)
                - __str__(self)
        📄 token_stream.py
            🏗️ Classes:
              • class TokenStream:
                - size(self)
                - is_empty(self)
                - first(self)
                - last(self)
                - at(self, index)
                - slice(self, start, stop)
                - __len__(self)
                - __iter__(self)
                - __getitem__(self, index)
                - __contains__(self, token)
                - __str__(self)
                - __repr__(self)
        📄 token_type.py
            🏗️ Classes:
              • class TokenType:
                - is_content(self)
                - is_whitespace(self)
                - is_terminal(self)
        📄 tokenization_result.py
            🏗️ Classes:
              • class TokenizationResult:
                - tokens(self)
                - token_count(self)
                - is_empty(self)
                - has_diagnostics(self)
                - __bool__(self)
                - __str__(self)
                - __repr__(self)
        📄 tokenizer.py
            🏗️ Classes:
              • class Tokenizer:
                - tokenize(self, source)
                - tokenize_many(self, sources)
                - supports(self, source)
        📄 tokenizer_token.py
            🏗️ Classes:
              • class TokenizerToken:
                - value(self)
                - is_content(self)
                - is_whitespace(self)
                - is_terminal(self)
                - length(self)
                - matches(self, value)
                - __str__(self)
                - __repr__(self)
      📂 types/
        📄 __init__.py
        📄 boolean_type.py
            🏗️ Classes:
              • class BooleanType:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __bool__(self)
                - __str__(self)
        📄 integer_type.py
            🏗️ Classes:
              • class IntegerType:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __int__(self)
                - __str__(self)
        📄 string_type.py
            🏗️ Classes:
              • class StringType:
                - __post_init__(self)
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_empty(self)
                - __str__(self)
                - __len__(self)
        📄 type.py
            🔹 Constants:
              • T
            🏗️ Classes:
              • class Type:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
      📂 validators/
        📄 __init__.py
        📄 composite_validator.py
            🏗️ Classes:
              • class CompositeValidator:
                - __init__(self, validators)
                - validators(self)
                - __len__(self)
                - __iter__(self)
                - validate(self, obj)
                - validate_many(self, objects)
        📄 validation_issue.py
            🏗️ Classes:
              • class ValidationSeverity:
              • class ValidationIssue:
                - is_error(self)
                - is_warning(self)
                - is_info(self)
        📄 validation_result.py
            🏗️ Classes:
              • class ValidationResult:
                - success(cls)
                - from_issues(cls, issues)
                - is_valid(self)
                - has_errors(self)
                - has_warnings(self)
                - has_info(self)
                - error_count(self)
                - warning_count(self)
                - info_count(self)
                - errors(self)
                - warnings(self)
                - info(self)
                - merge(self, other)
                - __bool__(self)
                - __len__(self)
        📄 validator.py
            🏗️ Classes:
              • class Validator:
                - validate(self, obj)
                - validate_many(self, objects)
                - supports(cls, obj)
        📄 validator_registry.py
            🏗️ Classes:
              • class ValidatorRegistry:
                - __init__(self)
                - register_validator(self, name, validator)
                - get_validator(self, name)
                - supporting(self, obj)
      📂 value_objects/
        📄 __init__.py
        📄 comparable_value.py
            🏗️ Classes:
              • class ComparableValue:
                - comparison_value(self)
                - __lt__(self, other)
                - __le__(self, other)
                - __gt__(self, other)
                - __ge__(self, other)
                - compare_to(self, other)
        📄 value_object.py
            🏗️ Classes:
              • class ValueObject:
                - same_value_as(self, other)
                - value(self)
                - __repr__(self)
      📂 version/
        📄 __init__.py
        📄 semantic_version.py
            🏗️ Classes:
              • class SemanticVersion:
                - __post_init__(self)
                - version(self)
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - increment_major(self)
                - increment_minor(self)
                - increment_patch(self)
                - __str__(self)
        📄 version.py
            🏗️ Classes:
              • class Version:
                - __post_init__(self)
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - matches(self, value)
                - __str__(self)
        📄 version_constraint.py
            🏗️ Classes:
              • class VersionConstraint:
                - __post_init__(self)
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
    📂 corpus/
      📄 __init__.py
      📄 gita.py
          ⚙️ Functions:
            • get_gita_verse(chapter, verse)
      📄 puranas.py
          ⚙️ Functions:
            • search_puranas(query)
      📄 vedas.py
          ⚙️ Functions:
            • search_vedas(query)
      📂 builders/
        📄 __init__.py
        📄 base_builder.py
            🔹 Constants:
              • T
            🏗️ Classes:
              • class BaseBuilder:
                - __init__(self)
                - _create_instance(self)
                - reset(self)
                - instance(self)
                - build(self)
                - clone(self)
                - from_instance(self, instance)
                - validate(self)
                - is_valid(self)
        📄 child_node_builder.py
            🏗️ Classes:
              • class ChildNodeBuilder:
                - _add_child(self, child, add_method)
                - _add_children(self, children, add_method)
        📄 corpus_builder.py
            🏗️ Classes:
              • class CorpusBuilder:
                - _create_instance(self)
                - with_metadata(self, metadata)
                - with_title(self, title)
                - with_description(self, description)
                - add_document(self, document)
                - add_documents(self, documents)
                - validate(self)
                - from_corpus(cls, corpus)
        📄 document_builder.py
            🏗️ Classes:
              • class DocumentBuilder:
                - _create_instance(self)
                - with_document_type(self, document_type)
                - with_page_range(self, start_page, end_page)
                - with_publisher(self, publisher)
                - with_edition(self, edition)
                - with_publication_year(self, year)
                - add_author(self, author)
                - add_editor(self, editor)
                - add_translator(self, translator)
                - add_section(self, section)
                - add_sections(self, sections)
                - from_document(cls, document)
        📄 line_builder.py
            🏗️ Classes:
              • class LineBuilder:
                - _create_instance(self)
                - validate(self)
                - with_line_number(self, number)
                - with_sequence_number(self, number)
                - with_visual_line_number(self, number)
                - with_indentation(self, level)
                - with_pada_number(self, number)
                - as_continuation(self, value)
                - as_refrain(self, value)
                - as_fragment(self, value)
                - with_language(self, language)
                - with_language_variant(self, language)
                - add_token(self, token)
                - add_tokens(self, tokens)
                - from_line(cls, line)
        📄 node_builder.py
            🏗️ Classes:
              • class NodeBuilder:
                - with_metadata(self, metadata)
                - with_title(self, title)
                - with_description(self, description)
                - with_identifier(self, identifier)
                - with_sequence_number(self, sequence_number)
                - with_parent_identifier(self, parent_identifier)
                - validate(self)
        📄 paragraph_builder.py
            🏗️ Classes:
              • class ParagraphBuilder:
                - _create_instance(self)
                - validate(self)
                - with_paragraph_number(self, number)
                - with_paragraph_type(self, paragraph_type)
                - with_language_variant(self, language)
                - as_translation(self, value)
                - as_commentary(self, value)
                - add_line(self, line)
                - add_lines(self, lines)
                - from_paragraph(cls, paragraph)
        📄 section_builder.py
            🏗️ Classes:
              • class SectionBuilder:
                - _create_instance(self)
                - with_section_type(self, section_type)
                - with_section_number(self, number)
                - add_section(self, section)
                - add_sections(self, sections)
                - add_verse(self, verse)
                - add_verses(self, verses)
                - from_section(cls, section)
        📄 token_builder.py
            🏗️ Classes:
              • class TokenBuilder:
                - _create_instance(self)
                - validate(self)
                - with_text(self, text)
                - with_normalized_text(self, text)
                - with_position(self, position)
                - with_token_type(self, token_type)
                - with_confidence(self, confidence)
                - with_source_offset(self, offset)
                - from_token(cls, token)
        📄 verse_builder.py
            🏗️ Classes:
              • class VerseBuilder:
                - _create_instance(self)
                - validate(self)
                - with_verse_number(self, number)
                - with_verse_type(self, verse_type)
                - with_meter(self, meter)
                - with_meter_name(self, meter_name)
                - add_paragraph(self, paragraph)
                - add_paragraphs(self, paragraphs)
                - from_verse(cls, verse)
      📂 enums/
        📄 corpus_type.py
            🏗️ Classes:
              • class CorpusType:
        📄 language.py
            🏗️ Classes:
              • class Language:
        📄 meter.py
            🏗️ Classes:
              • class Meter:
                - from_string(cls, value)
        📄 paragraph_type.py
            🏗️ Classes:
              • class ParagraphType:
                - from_string(cls, value)
        📄 script.py
            🏗️ Classes:
              • class Script:
        📄 token_type.py
            🏗️ Classes:
              • class TokenType:
                - from_string(cls, value)
        📄 verse_type.py
            🏗️ Classes:
              • class VerseType:
                - from_string(cls, value)
      📂 interfaces/
        📄 __init__.py
        📄 hierarchical.py
            🏗️ Classes:
              • class Hierarchical:
                - parent(self)
                - parent(self, value)
        📄 identifiable.py
            🏗️ Classes:
              • class Identifiable:
                - id(self)
        📄 metadata_provider.py
            🏗️ Classes:
              • class MetadataProvider:
                - metadata(self)
        📄 node_container.py
            🏗️ Classes:
              • class NodeContainer:
                - __len__(self)
                - __iter__(self)
        📄 serializable.py
            🏗️ Classes:
              • class Serializable:
                - to_dict(self)
      📂 iterators/
        📄 __init__.py
      📂 models/
        📄 base_metadata.py
            🏗️ Classes:
              • class BaseMetadata:
                - has_classification(self)
                - has_provenance(self)
                - add_keyword(self, keyword)
                - add_note(self, note)
                - metadata_dict(self)
        📄 base_node.py
            🏗️ Classes:
              • class BaseNode:
                - __init__(self, identifier, metadata)
                - id(self)
                - identifier(self)
                - __eq__(self, other)
                - __hash__(self)
                - __repr__(self)
        📄 base_node_metadata.py
            🏗️ Classes:
              • class BaseNodeMetadata:
                - has_identifier(self)
                - is_root(self)
                - hierarchy_dict(self)
                - to_dict(self)
                - __repr__(self)
        📄 classification.py
            🏗️ Classes:
              • class Classification:
                - is_unknown(self)
                - is_mixed(self)
                - set_language(self, language, confidence)
                - set_script(self, script, confidence)
                - set_corpus_type(self, corpus_type)
                - to_dict(self)
                - __repr__(self)
        📄 container_node.py
            🏗️ Classes:
              • class ContainerNode:
                - __init__(self, identifier, metadata)
                - children(self)
                - add_child(self, child)
                - remove_child(self, child)
                - extend(self, children)
                - clear_children(self)
                - child_count(self)
                - is_leaf(self)
                - first_child(self)
                - last_child(self)
                - __iter__(self)
                - __getitem__(self, index)
                - __len__(self)
        📄 corpus.py
            🏗️ Classes:
              • class Corpus:
                - __init__(self, id, metadata)
                - documents(self)
                - add_document(self, document)
                - remove_document(self, document)
                - clear_documents(self)
                - document_count(self)
                - first_document(self)
                - last_document(self)
                - to_dict(self)
                - __repr__(self)
        📄 corpus_metadata.py
            🏗️ Classes:
              • class CorpusMetadata:
                - has_classification(self)
                - has_provenance(self)
                - add_author(self, author)
                - add_editor(self, editor)
                - add_translator(self, translator)
                - add_keyword(self, keyword)
                - add_note(self, note)
                - merge(self, other)
                - to_dict(self)
        📄 document.py
            🏗️ Classes:
              • class Document:
                - __init__(self, identifier, metadata)
                - sections(self)
                - add_section(self, section)
                - remove_section(self, section)
                - section_count(self)
                - first_section(self)
                - last_section(self)
                - to_dict(self)
        📄 document_metadata.py
            🏗️ Classes:
              • class DocumentMetadata:
                - page_count(self)
                - has_page_range(self)
                - to_dict(self)
                - __repr__(self)
        📄 line.py
            🏗️ Classes:
              • class Line:
                - __init__(self, identifier, metadata)
                - tokens(self)
                - add_token(self, token)
                - remove_token(self, token)
                - token_count(self)
                - first_token(self)
                - last_token(self)
                - line_number(self)
                - language(self)
                - to_dict(self)
        📄 line_metadata.py
            🏗️ Classes:
              • class LineMetadata:
                - has_pada(self)
                - is_indented(self)
                - to_dict(self)
                - __repr__(self)
        📄 paragraph.py
            🏗️ Classes:
              • class Paragraph:
                - __init__(self, identifier, metadata)
                - lines(self)
                - add_line(self, line)
                - remove_line(self, line)
                - line_count(self)
                - first_line(self)
                - last_line(self)
                - paragraph_type(self)
                - language(self)
                - to_dict(self)
        📄 paragraph_metadata.py
            🏗️ Classes:
              • class ParagraphMetadata:
                - is_default(self)
                - to_dict(self)
                - __repr__(self)
        📄 section.py
            🏗️ Classes:
              • class Section:
                - __init__(self, identifier, metadata)
                - verses(self)
                - add_verse(self, verse)
                - remove_verse(self, verse)
                - verse_count(self)
                - first_verse(self)
                - last_verse(self)
                - to_dict(self)
        📄 section_metadata.py
            🏗️ Classes:
              • class SectionMetadata:
                - page_count(self)
                - has_page_range(self)
                - to_dict(self)
                - __repr__(self)
        📄 token.py
            🏗️ Classes:
              • class Token:
                - __init__(self, identifier, metadata)
                - text(self)
                - normalized_text(self)
                - token_type(self)
                - language(self)
                - position(self)
                - is_punctuation(self)
                - is_word(self)
                - to_dict(self)
        📄 token_metadata.py
            🏗️ Classes:
              • class TokenMetadata:
                - __init__(self, **kwargs)
                - token_index(self)
                - token_index(self, value)
                - has_normalized_text(self)
                - is_word(self)
                - is_whitespace(self)
                - to_dict(self)
                - __repr__(self)
        📄 verse.py
            🏗️ Classes:
              • class Verse:
                - __init__(self, identifier, metadata)
                - paragraphs(self)
                - add_paragraph(self, paragraph)
                - remove_paragraph(self, paragraph)
                - paragraph_count(self)
                - first_paragraph(self)
                - last_paragraph(self)
                - verse_type(self)
                - meter(self)
                - language(self)
                - to_dict(self)
        📄 verse_metadata.py
            🏗️ Classes:
              • class VerseMetadata:
                - page_count(self)
                - has_page_range(self)
                - has_audio(self)
                - has_image(self)
                - to_dict(self)
                - __repr__(self)
      📂 registries/
        📄 __init__.py
        📄 corpus_registry.py
            🏗️ Classes:
              • class CorpusRegistry:
                - __init__(self)
                - register(self, corpus)
                - unregister(self, corpus_id)
                - clear(self)
                - get(self, corpus_id)
                - exists(self, corpus_id)
                - all(self)
                - __contains__(self, corpus_id)
                - __iter__(self)
                - __len__(self)
                - __repr__(self)
      📂 validators/
        📄 base_corpus_validator.py
            🏗️ Classes:
              • class BaseCorpusValidator:
        📄 token_validator.py
            🏗️ Classes:
              • class TokenValidator:
                - validate(self, obj)
      📂 visitors/
        📄 __init__.py
      📂 alankara/
        📄 alankara_analysis.py
            🏗️ Classes:
              • class AlankaraAnalysis:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_alankara(self)
                - has_notes(self)
                - has_rule(self)
                - is_confident(self)
                - __str__(self)
        📄 alankara_analysis_collection.py
            🏗️ Classes:
              • class AlankaraAnalysisCollection:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - count(self)
                - is_empty(self)
                - first(self)
                - add(self, analysis)
                - extend(self, other)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 alankara_context.py
            🏗️ Classes:
              • class AlankaraContext:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_source(self)
                - has_metadata(self)
                - metadata_count(self)
                - recursive(self)
                - multiple_analyses_enabled(self)
                - get(self, key, default)
                - __str__(self)
        📄 alankara_diagnostic.py
            🏗️ Classes:
              • class AlankaraDiagnostic:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_info(self)
                - is_warning(self)
                - is_error(self)
                - has_rule(self)
                - has_location(self)
                - __str__(self)
        📄 alankara_parser.py
            🔹 Constants:
              • _PUNCT_RE
            🏗️ Classes:
              • class AlankaraStructure:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - token_count(self)
                - has_tokens(self)
                - get(self, key, default)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
                - normalize(cls, identifier, text)
              • class AlankaraParseResult:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - cue_count(self)
                - has_cues(self)
                - first_cue(self)
                - get(self, key, default)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
              • class AlankaraParser:
                - normalize(self, identifier, text)
                - _extract_cues(self, text, metadata)
                - parse(self, identifier, text)
        📄 alankara_resolver.py
            🏗️ Classes:
              • class AlankaraResolver:
                - __init__(self, strategy)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - strategy(self)
                - analyze(self, context)
                - __str__(self)
        📄 alankara_result.py
            🏗️ Classes:
              • class AlankaraResult:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - subject(self)
                - source(self)
                - language(self)
                - script(self)
                - has_analyses(self)
                - analysis_count(self)
                - first_analysis(self)
                - result(self)
                - has_diagnostics(self)
                - diagnostic_count(self)
                - has_errors(self)
                - has_warnings(self)
                - first_diagnostic(self)
                - resolved(self)
                - unresolved(self)
                - is_confident(self)
                - best_analysis(self)
                - __str__(self)
        📄 alankara_rule.py
            🏗️ Classes:
              • class AlankaraRule:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - applies_to(self, context)
                - apply(self, context)
                - __str__(self)
              • class UpamaRule:
                - display_name(self)
                - display_description(self)
                - applies_to(self, context)
                - apply(self, context)
              • class RupakaRule:
                - display_name(self)
                - display_description(self)
                - applies_to(self, context)
                - apply(self, context)
              • class AnuprasaRule:
                - display_name(self)
                - display_description(self)
                - applies_to(self, context)
                - apply(self, context)
              • class YamakaRule:
                - display_name(self)
                - display_description(self)
                - applies_to(self, context)
                - apply(self, context)
              • class ShleshaRule:
                - display_name(self)
                - display_description(self)
                - applies_to(self, context)
                - apply(self, context)
        📄 alankara_rule_set.py
            🏗️ Classes:
              • class AlankaraRuleSet:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_empty(self)
                - count(self)
                - add(self, rule)
                - _candidate_key(self, candidate)
                - apply(self, context)
                - __len__(self)
                - __iter__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 alankara_strategy.py
            🏗️ Classes:
              • class AlankaraStrategy:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, context)
                - __str__(self)
        📄 default_alankara_resolver.py
            🏗️ Classes:
              • class DefaultAlankaraResolver:
                - __init__(self, strategy)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, context)
        📄 default_alankara_rule_set.py
            🔹 Constants:
              • DEFAULT_ALANKARA_RULES
            ⚙️ Functions:
              • default_alankara_rule_set()
        📄 default_alankara_strategy.py
            🏗️ Classes:
              • class DefaultAlankaraStrategy:
                - __init__(self, rule_set)
                - rule_set(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - _to_analysis_collection(self, context, candidates)
                - analyze(self, context)
      📂 chandas/
        📄 chandas_analysis.py
            🏗️ Classes:
              • class ChandasAnalysis:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_meter(self)
                - has_notes(self)
                - has_rule(self)
                - is_confident(self)
                - __str__(self)
        📄 chandas_analysis_collection.py
            🏗️ Classes:
              • class ChandasAnalysisCollection:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - count(self)
                - is_empty(self)
                - first(self)
                - add(self, analysis)
                - extend(self, other)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 chandas_context.py
            🏗️ Classes:
              • class ChandasContext:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_source(self)
                - has_metadata(self)
                - metadata_count(self)
                - recursive(self)
                - multiple_analyses_enabled(self)
                - get(self, key, default)
                - __str__(self)
        📄 chandas_diagnostic.py
            🏗️ Classes:
              • class ChandasDiagnostic:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_info(self)
                - is_warning(self)
                - is_error(self)
                - has_rule(self)
                - has_location(self)
                - __str__(self)
        📄 chandas_resolver.py
            🏗️ Classes:
              • class ChandasResolver:
                - __init__(self, strategy)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - strategy(self)
                - analyze(self, context)
                - __str__(self)
        📄 chandas_result.py
            🏗️ Classes:
              • class ChandasResult:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - subject(self)
                - source(self)
                - language(self)
                - script(self)
                - has_analyses(self)
                - analysis_count(self)
                - first_analysis(self)
                - result(self)
                - has_diagnostics(self)
                - diagnostic_count(self)
                - has_errors(self)
                - has_warnings(self)
                - first_diagnostic(self)
                - resolved(self)
                - unresolved(self)
                - is_confident(self)
                - best_analysis(self)
                - __str__(self)
        📄 chandas_rule.py
            🏗️ Classes:
              • class ChandasRule:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - applies_to(self, context)
                - apply(self, context)
                - __str__(self)
              • class MeterHintRule:
                - display_name(self)
                - display_description(self)
                - applies_to(self, context)
                - apply(self, context)
              • class VerseHeuristicRule:
                - display_name(self)
                - display_description(self)
                - _count_syllables(self, text)
                - _count_padas(self, text)
                - _meter_from_syllables(self, syllables, pada_count)
                - applies_to(self, context)
                - apply(self, context)
        📄 chandas_rule_set.py
            🏗️ Classes:
              • class ChandasRuleSet:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_empty(self)
                - count(self)
                - add(self, rule)
                - _candidate_key(self, candidate)
                - apply(self, context)
                - __len__(self)
                - __iter__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 chandas_strategy.py
            🏗️ Classes:
              • class ChandasStrategy:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, context)
                - __str__(self)
        📄 default_chandas_resolver.py
            🏗️ Classes:
              • class DefaultChandasResolver:
                - __init__(self, strategy)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, context)
        📄 default_chandas_rule_set.py
            🔹 Constants:
              • DEFAULT_CHANDAS_RULES
            ⚙️ Functions:
              • default_chandas_rule_set()
        📄 default_chandas_strategy.py
            🏗️ Classes:
              • class DefaultChandasStrategy:
                - __init__(self, rule_set)
                - rule_set(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - _to_analysis_collection(self, context, candidates)
                - analyze(self, context)
      📂 derivation/
        📄 default_derivation_repository.py
            🔹 Constants:
              • DEFAULT_DERIVATION_PATTERNS
            🏗️ Classes:
              • class DefaultDerivationRepository:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - get(self, identifier)
                - find_by_category(self, category)
                - search(self, query)
                - all(self)
                - contains(self, identifier)
                - count(self)
        📄 default_derivation_resolver.py
            🏗️ Classes:
              • class DefaultDerivationResolver:
                - __init__(self, strategy)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, context)
        📄 default_derivation_rule_set.py
            🔹 Constants:
              • DEFAULT_DERIVATION_RULES
            ⚙️ Functions:
              • default_derivation_rule_set()
        📄 default_derivation_strategy.py
            🏗️ Classes:
              • class DefaultDerivationStrategy:
                - __init__(self, rule_set, repository)
                - rule_set(self)
                - repository(self)
                - ranker(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - _template_patterns(self, query)
                - _best_pattern_name(self, query)
                - _build_outputs(self, context, candidates, source_pattern_name)
                - _rank_best_pattern_name(self, outputs, fallback)
                - _relabel_outputs(self, outputs, pattern_name)
                - analyze(self, context)
        📄 derivation_analysis.py
            🏗️ Classes:
              • class DerivationAnalysis:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_rule(self)
                - has_notes(self)
                - is_confident(self)
                - __str__(self)
        📄 derivation_analysis_collection.py
            🏗️ Classes:
              • class DerivationAnalysisCollection:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - count(self)
                - is_empty(self)
                - first(self)
                - add(self, analysis)
                - extend(self, other)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 derivation_context.py
            🏗️ Classes:
              • class DerivationContext:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_source(self)
                - has_metadata(self)
                - metadata_count(self)
                - recursive(self)
                - multiple_derivations_enabled(self)
                - get(self, key, default)
                - __str__(self)
        📄 derivation_diagnostic.py
            🏗️ Classes:
              • class DerivationDiagnostic:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_info(self)
                - is_warning(self)
                - is_error(self)
                - has_rule(self)
                - has_location(self)
                - __str__(self)
        📄 derivation_output.py
            🏗️ Classes:
              • class DerivationOutput:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_pada(self)
                - has_notes(self)
                - has_source_pattern(self)
                - is_confident(self)
                - __str__(self)
        📄 derivation_output_collection.py
            🏗️ Classes:
              • class DerivationOutputCollection:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - count(self)
                - is_empty(self)
                - first(self)
                - last(self)
                - add(self, output)
                - extend(self, other)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 derivation_pattern.py
            🏗️ Classes:
              • class DerivationPattern:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_category(self)
                - has_notes(self)
                - is_active(self)
                - __str__(self)
        📄 derivation_pattern_collection.py
            🏗️ Classes:
              • class DerivationPatternCollection:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - count(self)
                - is_empty(self)
                - first(self)
                - last(self)
                - add(self, pattern)
                - extend(self, other)
                - get_by_identifier(self, identifier)
                - find_by_category(self, category)
                - search(self, query)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 derivation_pattern_ranker.py
            🏗️ Classes:
              • class RankedDerivationPattern:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
              • class RankedDerivationPatternCollection:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_empty(self)
                - count(self)
                - first(self)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
              • class DerivationPatternRanker:
                - __init__(self, repository)
                - repository(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - _normalize_outputs(self, outputs)
                - _output_query(self, output)
                - _score_pattern(self, pattern, output)
                - rank(self, outputs)
                - best(self, outputs)
                - rank_patterns(self, outputs)
        📄 derivation_repository.py
            🏗️ Classes:
              • class DerivationRepository:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - get(self, identifier)
                - find_by_category(self, category)
                - search(self, query)
                - all(self)
                - contains(self, identifier)
                - count(self)
        📄 derivation_resolver.py
            🏗️ Classes:
              • class DerivationResolver:
                - __init__(self, strategy)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - strategy(self)
                - analyze(self, context)
                - __str__(self)
        📄 derivation_result.py
            🏗️ Classes:
              • class DerivationResult:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - subject(self)
                - dhatu(self)
                - pratyaya(self)
                - source(self)
                - language(self)
                - script(self)
                - has_outputs(self)
                - output_count(self)
                - best_output(self)
                - result(self)
                - analyses(self)
                - has_analyses(self)
                - analysis_count(self)
                - best_analysis(self)
                - has_diagnostics(self)
                - diagnostic_count(self)
                - first_diagnostic(self)
                - has_errors(self)
                - has_warnings(self)
                - resolved(self)
                - unresolved(self)
                - is_confident(self)
                - __str__(self)
        📄 derivation_rule.py
            🏗️ Classes:
              • class DerivationRule:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - applies_to(self, context)
                - apply(self, context)
                - __str__(self)
        📄 derivation_rule_set.py
            🏗️ Classes:
              • class DerivationRuleSet:
                - apply(self, context)
        📄 derivation_strategy.py
            🏗️ Classes:
              • class DerivationStrategy:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, context)
                - __str__(self)
        📄 dhatu_pratyaya_concat_rule.py
            🏗️ Classes:
              • class DhatuPratyayaConcatRule:
                - display_name(self)
                - display_description(self)
                - applies_to(self, context)
                - apply(self, context)
        📄 dhatu_pratyaya_sandhi_rule.py
            🏗️ Classes:
              • class DhatuPratyayaSandhiRule:
                - display_name(self)
                - display_description(self)
                - _key(self, context)
                - applies_to(self, context)
                - apply(self, context)
        📄 hint_based_derivation_rule.py
            🏗️ Classes:
              • class HintBasedDerivationRule:
                - display_name(self)
                - display_description(self)
                - applies_to(self, context)
                - apply(self, context)
        📄 pratyaya_to_derivation_bridge.py
            🏗️ Classes:
              • class DerivationCandidate:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_pada(self)
                - has_notes(self)
                - has_pattern(self)
                - is_confident(self)
                - __str__(self)
              • class DerivationCandidateCollection:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - count(self)
                - is_empty(self)
                - first(self)
                - add(self, candidate)
                - extend(self, other)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
              • class PratyayaToDerivationBridge:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - _normalize_analysis(self, item)
                - _analysis_iter(self, pratyaya_source)
                - _pattern_for(self, pratyaya)
                - bridge(self, dhatu, pratyaya_source)
                - to_payloads(self, dhatu, pratyaya_source)
      📂 dhatu/
        📄 default_dhatu_repository.py
            🏗️ Classes:
              • class DefaultDhatuRepository:
                - __init__(self, dhatus)
                - _validate_dhatu(dhatu)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - get(self, identifier)
                - find_by_root(self, root)
                - find_by_gana(self, gana)
                - search(self, query)
                - all(self)
                - contains(self, identifier)
                - count(self)
                - register(self, dhatu)
                - register_many(self, dhatus)
                - remove(self, identifier)
                - clear(self)
                - __len__(self)
                - __contains__(self, identifier)
                - __str__(self)
        📄 default_dhatu_resolver.py
            🏗️ Classes:
              • class DefaultDhatuResolver:
                - __init__(self, strategy)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, context)
        📄 default_dhatu_rule_set.py
            🔹 Constants:
              • DEFAULT_DHATU_RULES
            ⚙️ Functions:
              • default_dhatu_rule_set()
        📄 default_dhatu_service.py
            🏗️ Classes:
              • class DefaultDhatuService:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, context)
                - resolve(self, context)
                - __str__(self)
        📄 default_dhatu_strategy.py
            🏗️ Classes:
              • class DefaultDhatuStrategy:
                - __init__(self, rule_set)
                - rule_set(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, context)
        📄 dhatu.py
            🏗️ Classes:
              • class Dhatu:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_gana(self)
                - has_meaning(self)
                - __str__(self)
        📄 dhatu_analysis.py
            🏗️ Classes:
              • class DhatuAnalysis:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_rule(self)
                - has_notes(self)
                - __str__(self)
        📄 dhatu_analysis_collection.py
            🏗️ Classes:
              • class DhatuAnalysisCollection:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - count(self)
                - is_empty(self)
                - first(self)
                - add(self, analysis)
                - extend(self, other)
                - __len__(self)
                - __iter__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 dhatu_collection.py
            🏗️ Classes:
              • class DhatuCollection:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - count(self)
                - is_empty(self)
                - first(self)
                - add(self, dhatu)
                - extend(self, other)
                - get_by_root(self, root)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 dhatu_context.py
            🏗️ Classes:
              • class DhatuContext:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_source(self)
                - has_metadata(self)
                - metadata_count(self)
                - recursive(self)
                - multiple_analyses_enabled(self)
                - get(self, key, default)
                - __str__(self)
        📄 dhatu_diagnostic.py
            🏗️ Classes:
              • class DhatuDiagnostic:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_info(self)
                - is_warning(self)
                - is_error(self)
                - has_rule(self)
                - has_location(self)
                - __str__(self)
        📄 dhatu_factory.py
            🏗️ Classes:
              • class DhatuFactory:
                - create_dhatu(specification)
                - create_dhatus(cls, specification)
                - create_collection(cls, specification)
                - create_default_collection(cls)
        📄 dhatu_gana.py
            🔹 Constants:
              • BVADI
              • ADADI
              • JUHOTYADI
              • DIVADI
              • SVADI
              • TUDADI
              • RUDHADI
              • TANADI
              • KRYADI
              • CURADI
            🏗️ Classes:
              • class DhatuGana:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
        📄 dhatu_repository.py
            🏗️ Classes:
              • class DhatuRepository:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - get(self, identifier)
                - find_by_root(self, root)
                - find_by_gana(self, gana)
                - search(self, query)
                - all(self)
                - contains(self, identifier)
                - count(self)
        📄 dhatu_resolver.py
            🏗️ Classes:
              • class DhatuResolver:
                - __init__(self, strategy)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - strategy(self)
                - analyze(self, context)
                - __str__(self)
        📄 dhatu_result.py
            🏗️ Classes:
              • class DhatuResult:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - subject(self)
                - source(self)
                - language(self)
                - script(self)
                - result(self)
                - analysis_count(self)
                - has_analyses(self)
                - first_analysis(self)
                - has_diagnostics(self)
                - diagnostic_count(self)
                - has_errors(self)
                - has_warnings(self)
                - first_diagnostic(self)
                - resolved(self)
                - unresolved(self)
                - is_confident(self)
                - best_analysis(self)
                - __str__(self)
        📄 dhatu_rule.py
            🏗️ Classes:
              • class DhatuRule:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - applies_to(self, context)
                - apply(self, context)
                - __str__(self)
        📄 dhatu_rule_set.py
            🏗️ Classes:
              • class DhatuRuleSet:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_empty(self)
                - count(self)
                - add(self, rule)
                - apply(self, context)
                - __len__(self)
                - __iter__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 dhatu_service.py
            🏗️ Classes:
              • class DhatuService:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, context)
                - resolve(self, context)
                - __str__(self)
        📄 dhatu_specification.py
            🔹 Constants:
              • CANONICAL_DHATU_SPECIFICATION
            🏗️ Classes:
              • class DhatuSpecification:
        📄 dhatu_strategy.py
            🏗️ Classes:
              • class DhatuStrategy:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, context)
                - __str__(self)
        📄 gana_match_rule.py
            🏗️ Classes:
              • class GanaMatchRule:
                - display_name(self)
                - display_description(self)
                - _extract_text(self, context)
                - applies_to(self, context)
                - apply(self, context)
        📄 known_dhatu_rule.py
            🏗️ Classes:
              • class KnownDhatuRule:
                - display_name(self)
                - display_description(self)
                - _extract_text(self, context)
                - _hinted(self, context)
                - applies_to(self, context)
                - apply(self, context)
      📂 grammar/
        📄 default_grammar_analysis_strategy.py
            🏗️ Classes:
              • class DefaultGrammarAnalysisStrategy:
                - __init__(self, rule_set)
                - rule_set(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, subject)
        📄 default_grammar_analyzer.py
            🏗️ Classes:
              • class DefaultGrammarAnalyzer:
                - __init__(self, strategy)
                - display_name(self)
                - display_text(self)
                - display_description(self)
        📄 default_grammar_rule_set.py
            ⚙️ Functions:
              • default_grammar_rule_set()
        📄 grammar_analysis.py
            🏗️ Classes:
              • class GrammarAnalysis:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_outputs(self)
                - output_count(self)
                - is_confident(self)
                - has_notes(self)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 grammar_analysis_collection.py
            🏗️ Classes:
              • class GrammarAnalysisCollection:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_empty(self)
                - count(self)
                - has_analyses(self)
                - first(self)
                - last(self)
                - add(self, analysis)
                - extend(self, other)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 grammar_analysis_result.py
            🏗️ Classes:
              • class GrammarAnalysisResult:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_outputs(self)
                - output_count(self)
                - is_confident(self)
                - first_output(self)
                - last_output(self)
                - result(self)
                - __str__(self)
        📄 grammar_analysis_strategy.py
            🏗️ Classes:
              • class GrammarAnalysisStrategy:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, subject)
        📄 grammar_analyzer.py
            🏗️ Classes:
              • class GrammarAnalyzer:
                - __init__(self, strategy)
                - strategy(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, subject)
                - __str__(self)
        📄 grammar_category.py
            🏗️ Classes:
              • class GrammarCategory:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_abbreviation(self)
                - has_description(self)
                - __str__(self)
        📄 grammar_feature.py
            🏗️ Classes:
              • class GrammarFeature:
                - grammatical_domain(self)
                - is_role(self)
                - is_relation(self)
                - is_feature(self)
                - is_rule(self)
        📄 grammar_relation.py
            🏗️ Classes:
              • class GrammarRelation:
                - grammatical_domain(self)
                - is_role(self)
                - is_relation(self)
                - is_feature(self)
                - is_rule(self)
        📄 grammar_role.py
            🏗️ Classes:
              • class GrammarRole:
                - grammatical_domain(self)
                - is_role(self)
                - is_relation(self)
                - is_feature(self)
                - is_rule(self)
        📄 grammar_rule.py
            🏗️ Classes:
              • class GrammarRule:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - applies_to(self, subject)
                - apply(self, subject)
                - __str__(self)
        📄 grammar_rule_set.py
            🏗️ Classes:
              • class GrammarRuleSet:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_empty(self)
                - count(self)
                - add(self, rule)
                - apply(self, subject)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 karma_grammar_rule.py
            🏗️ Classes:
              • class KarmaGrammarRule:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - _extract_text(self, subject)
                - applies_to(self, subject)
                - apply(self, subject)
        📄 karta_grammar_rule.py
            🏗️ Classes:
              • class KartaGrammarRule:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - _extract_text(self, subject)
                - applies_to(self, subject)
                - apply(self, subject)
      📂 knowledge_graph/
        📄 default_knowledge_graph_resolver.py
            🏗️ Classes:
              • class DefaultKnowledgeGraphResolver:
                - __init__(self, strategy)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, context)
        📄 default_knowledge_graph_strategy.py
            🏗️ Classes:
              • class DefaultKnowledgeGraphStrategy:
                - __init__(self, builder)
                - builder(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - _merge_source_graphs(self, context)
                - analyze(self, context)
        📄 knowledge_graph.py
            🏗️ Classes:
              • class KnowledgeGraph:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - node_count(self)
                - edge_count(self)
                - is_empty(self)
                - has_nodes(self)
                - has_edges(self)
                - get_node(self, identifier)
                - get_edge(self, identifier)
                - add_node(self, node)
                - add_edge(self, edge)
                - merge(self, other)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 knowledge_graph_builder.py
            🏗️ Classes:
              • class KnowledgeGraphBuilder:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - _node(self, identifier, label, node_type, description, payload, confidence)
                - from_semantic(self, identifier, semantic)
                - from_chandas(self, identifier, chandas)
                - from_alankara(self, identifier, alankara)
                - from_derivation(self, identifier, derivation)
        📄 knowledge_graph_context.py
            🏗️ Classes:
              • class KnowledgeGraphContext:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - get(self, key, default)
                - __str__(self)
        📄 knowledge_graph_diagnostic.py
            🏗️ Classes:
              • class KnowledgeGraphDiagnostic:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_info(self)
                - is_warning(self)
                - is_error(self)
                - __str__(self)
        📄 knowledge_graph_edge.py
            🏗️ Classes:
              • class KnowledgeGraphEdge:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_payload(self)
                - __str__(self)
        📄 knowledge_graph_node.py
            🏗️ Classes:
              • class KnowledgeGraphNode:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_payload(self)
                - __str__(self)
        📄 knowledge_graph_resolver.py
            🏗️ Classes:
              • class KnowledgeGraphResolver:
                - __init__(self, strategy)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - strategy(self)
                - analyze(self, context)
                - __str__(self)
        📄 knowledge_graph_result.py
            🏗️ Classes:
              • class KnowledgeGraphResult:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - subject(self)
                - source(self)
                - language(self)
                - script(self)
                - has_graph(self)
                - node_count(self)
                - edge_count(self)
                - result(self)
                - has_diagnostics(self)
                - diagnostic_count(self)
                - first_diagnostic(self)
                - resolved(self)
                - unresolved(self)
                - is_confident(self)
                - __str__(self)
        📄 knowledge_graph_strategy.py
            🏗️ Classes:
              • class KnowledgeGraphStrategy:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, context)
                - __str__(self)
      📂 lexical/
        📄 default_lexical_repository.py
            🏗️ Classes:
              • class DefaultLexicalRepository:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - get_entry(self, headword)
                - find_entries_by_lemma(self, lemma)
                - find_entries_by_word_form(self, word_form)
                - find_senses(self, headword)
                - search(self, query)
                - all_entries(self)
                - count(self)
                - __str__(self)
        📄 default_lexical_resolution_strategy.py
            🏗️ Classes:
              • class DefaultLexicalResolutionStrategy:
                - __init__(self, lookup_engine)
                - lookup_engine(self)
                - resolve(self, context)
                - display_name(self)
                - display_description(self)
        📄 default_lexical_service.py
            🏗️ Classes:
              • class DefaultLexicalService:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
        📄 dictionary_entry.py
            🏗️ Classes:
              • class DictionaryEntry:
                - __post_init__(self)
                - has_senses(self)
                - sense_count(self)
                - is_empty(self)
        📄 dictionary_sense.py
            🏗️ Classes:
              • class DictionarySense:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - example_count(self)
                - has_examples(self)
                - has_source(self)
                - has_grammatical_label(self)
                - has_transliteration(self)
                - __str__(self)
        📄 lemma.py
            🏗️ Classes:
              • class Lemma:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_transliteration(self)
                - __str__(self)
        📄 lexeme.py
            🏗️ Classes:
              • class Lexeme:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - alias_count(self)
                - has_aliases(self)
                - has_transliteration(self)
                - matches(self, text)
                - __str__(self)
        📄 lexical_entry.py
            🏗️ Classes:
              • class LexicalEntry:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - lemma(self)
                - entry_count(self)
                - sense_count(self)
                - word_form_count(self)
                - relation_count(self)
                - has_dictionary_entries(self)
                - has_dictionary_senses(self)
                - has_word_forms(self)
                - has_relations(self)
                - __str__(self)
        📄 lexical_entry_collection.py
            🏗️ Classes:
              • class LexicalEntryCollection:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - count(self)
                - is_empty(self)
                - has_entries(self)
                - first(self)
                - last(self)
                - add(self, entry)
                - extend(self, other)
                - contains(self, identifier)
                - get(self, identifier)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __contains__(self, entry)
                - __str__(self)
        📄 lexical_lookup_engine.py
            🏗️ Classes:
              • class LexicalLookupEngine:
                - __init__(self, repository, ranking_policy)
                - repository(self)
                - ranking_policy(self)
                - lookup(self, context)
        📄 lexical_relation.py
            🏗️ Classes:
              • class LexicalRelation:
                - __post_init__(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - identity(self)
                - has_notes(self)
                - to_dict(self)
                - __str__(self)
        📄 lexical_repository.py
            🏗️ Classes:
              • class LexicalRepository:
                - __init__(self, repository)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - repository(self)
                - get_entry(self, headword)
                - find_entries_by_lemma(self, lemma)
                - find_entries_by_word_form(self, word_form)
                - find_senses(self, headword)
                - search(self, query)
                - all_entries(self)
                - count(self)
        📄 lexical_resolution_result.py
            🏗️ Classes:
              • class LexicalResolutionResult:
                - has_candidates(self)
                - candidate_count(self)
                - preferred_candidate(self)
                - preferred_entry(self)
                - preferred_sense(self)
                - has_entry(self)
                - has_sense(self)
                - canonical_context(self)
                - canonical_source(self)
                - headword(self)
                - lemma(self)
                - lexeme(self)
                - definition(self)
                - glossary(self)
                - resolved(self)
                - unresolved(self)
                - is_unique(self)
                - is_ambiguous(self)
                - is_confident(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
        📄 lexical_resolution_strategy.py
            🏗️ Classes:
              • class LexicalResolutionStrategy:
                - resolve(self, context)
        📄 lexical_resolver.py
            🏗️ Classes:
              • class LexicalResolver:
                - __init__(self, strategy)
                - strategy(self)
                - resolve(self, context)
                - display_name(self)
                - display_description(self)
        📄 lexical_service.py
            🏗️ Classes:
              • class LexicalService:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - lookup_engine(self)
                - resolve(self, context)
                - contribute(self, aggregate, context)
                - get_entry(self, headword)
                - lookup_lemma(self, lemma)
                - lookup_word_form(self, word_form)
                - lookup_senses(self, headword)
                - search(self, query)
                - all_entries(self)
                - count(self)
                - __str__(self)
        📄 lexical_source.py
            🏗️ Classes:
              • class LexicalSource:
                - __post_init__(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_version(self)
                - has_description(self)
                - has_url(self)
                - canonical_name(self)
                - to_dict(self)
                - __str__(self)
        📄 lookup_candidate.py
            🏗️ Classes:
              • class LookupCandidate:
                - identifier(self)
                - headword(self)
                - has_sense(self)
                - confidence(self)
                - __str__(self)
        📄 lookup_ranking_policy.py
            🏗️ Classes:
              • class LookupRankingPolicy:
                - rank(self, candidates)
              • class DefaultLookupRankingPolicy:
                - rank(self, candidates)
        📄 token.py
            🏗️ Classes:
              • class Token:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - lemma(self)
                - canonical_form(self)
                - is_lemma(self)
                - __str__(self)
        📄 word_form.py
            🏗️ Classes:
              • class WordForm:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - canonical_form(self)
                - is_lemma(self)
                - __str__(self)
        📂 adapters/
          📄 __init__.py
          📄 in_memory_monier_williams_adapter.py
              🏗️ Classes:
                • class InMemoryMonierWilliamsAdapter:
                  - __init__(self, records)
                  - lookup(self, headword)
                  - search(self, query)
                  - all_records(self)
                  - count(self)
          📄 monier_williams_adapter.py
              🏗️ Classes:
                • class MonierWilliamsAdapter:
                  - source(self)
                  - lookup(self, headword)
                  - search(self, query)
                  - all_records(self)
                  - count(self)
                  - normalize_headword(value)
                  - normalize_record(cls, record)
                  - normalize_records(cls, records)
          📄 monier_williams_mapper.py
              🏗️ Classes:
                • class MonierWilliamsMapper:
                  - to_entry(cls, record)
                  - to_sense(cls, record)
          📄 monier_williams_record.py
              🏗️ Classes:
                • class MonierWilliamsRecord:
        📂 validators/
          📄 base_lexical_validator.py
              🏗️ Classes:
                • class BaseLexicalValidator:
                  - validate(self, obj)
                  - success()
                  - result_from_issues(*issues)
                  - error()
                  - warning()
                  - info()
                  - is_blank(value)
                  - text_error()
          📄 dictionary_entry_validator.py
              🏗️ Classes:
                • class DictionaryEntryValidator:
                  - supports(cls, obj)
                  - validate(self, obj)
          📄 dictionary_sense_validator.py
              🏗️ Classes:
                • class DictionarySenseValidator:
                  - supports(cls, obj)
                  - validate(self, obj)
          📄 lexeme_validator.py
              🏗️ Classes:
                • class LexemeValidator:
                  - supports(cls, obj)
                  - validate(self, obj)
          📄 lexical_composite_validator.py
              🏗️ Classes:
                • class LexicalCompositeValidator:
                  - __init__(self, validators)
                  - validators(self)
                  - validate(self, value)
          📄 lexical_relation_validator.py
              🏗️ Classes:
                • class LexicalRelationValidator:
                  - supports(cls, obj)
                  - validate(self, obj)
          📄 lexical_source_validator.py
              🏗️ Classes:
                • class LexicalSourceValidator:
                  - supports(cls, obj)
                  - validate(self, obj)
          📄 lexical_validator_registry.py
              🏗️ Classes:
                • class LexicalValidatorRegistry:
                  - __init__(self, validators)
                  - _register_defaults(self)
                  - _infer_model_type(validator)
                  - register(self, model_type, validator)
                  - unregister(self, model_type)
                  - get(self, model_type)
                  - resolve(self, value_or_type)
                  - contains(self, model_type)
                  - clear(self)
                  - __len__(self)
                  - __contains__(self, model_type)
                  - items(self)
      📂 morphology/
        📄 default_morphological_analyzer.py
            🏗️ Classes:
              • class DefaultMorphologicalAnalyzer:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - rules(self)
                - analyze(self, word_form)
                - __str__(self)
        📄 default_morphological_repository.py
            🏗️ Classes:
              • class DefaultMorphologicalRepository:
                - __post_init__(self)
                - count(self)
                - vibhakti(self)
                - vacana(self)
                - linga(self)
                - purusha(self)
                - lakara(self)
                - pada(self)
                - prayoga(self)
                - nominal_categories(self)
                - verbal_categories(self)
                - all_categories(self)
                - morphological_rule_set(self)
                - morphological_analyzer(self)
                - count(self)
        📄 default_morphological_resolution_kernel.py
            🏗️ Classes:
              • class DefaultMorphologicalResolutionKernel:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - resolution_strategy(self)
                - kernel(self)
                - resolve(self, context)
                - __call__(self, context)
                - __str__(self)
        📄 default_morphological_resolution_strategy.py
            🏗️ Classes:
              • class DefaultMorphologicalResolutionStrategy:
                - display_name(self)
                - display_description(self)
                - resolve(self, context)
        📄 default_morphological_rule_set.py
            ⚙️ Functions:
              • default_morphological_rule_set()
        📄 default_morphological_service.py
            🏗️ Classes:
              • class DefaultMorphologicalService:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - morphological_repository(self)
                - resolution_kernel(self)
                - analyzer(self)
                - analyze(self, word_form)
                - resolve(self, context)
                - __call__(self, context)
                - vibhakti(self)
                - vacana(self)
                - linga(self)
                - purusha(self)
                - lakara(self)
                - pada(self)
                - prayoga(self)
                - nominal_categories(self)
                - verbal_categories(self)
                - all_categories(self)
                - rule_set(self)
                - morphological_rule_set(self)
                - count(self)
                - __str__(self)
        📄 grammatical_category.py
            🏗️ Classes:
              • class GrammaticalCategory:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_abbreviation(self)
                - has_description(self)
                - __str__(self)
        📄 grammatical_category_collection.py
            🏗️ Classes:
              • class GrammaticalCategoryCollection:
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __contains__(self, category)
                - count(self)
                - is_empty(self)
                - first(self)
                - last(self)
                - find(self, identifier)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
        📄 indeclinable_avyaya_category.py
            🏗️ Classes:
              • class IndeclinableAvyayaCategory:
                - grammatical_domain(self)
                - sanskrit_domain(self)
                - is_nominal(self)
                - is_verbal(self)
                - is_indeclinable(self)
        📄 lakara.py
            🏗️ Classes:
              • class Lakara:
        📄 linga.py
            🏗️ Classes:
              • class Linga:
        📄 morphological_analysis.py
            🏗️ Classes:
              • class MorphologicalAnalysis:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_confident(self)
                - has_alternatives(self)
                - alternative_count(self)
                - feature_count(self)
                - is_nominal(self)
                - is_verbal(self)
                - is_indeclinable(self)
                - __iter__(self)
                - __len__(self)
                - __str__(self)
        📄 morphological_analysis_collection.py
            🏗️ Classes:
              • class MorphologicalAnalysisCollection:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_empty(self)
                - count(self)
                - has_analyses(self)
                - add(self, analysis)
                - extend(self, other)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 morphological_analyzer.py
            🏗️ Classes:
              • class MorphologicalAnalyzer:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, word_form)
        📄 morphological_context.py
            🏗️ Classes:
              • class MorphologicalContext:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_lexical_result(self)
                - has_dhatu_result(self)
                - has_canonical_repository(self)
                - has_dhatu_repository(self)
                - canonical_entry(self)
                - canonical_sense(self)
                - dhatu(self)
                - root(self)
                - lemma(self)
                - __str__(self)
        📄 morphological_dhatu_resolver.py
            🏗️ Classes:
              • class MorphologicalDhatuResolver:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - resolve_by_root(self, root)
                - resolve_by_identifier(self, identifier)
                - search(self, query)
        📄 morphological_features.py
            🏗️ Classes:
              • class MorphologicalFeatures:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_nominal(self)
                - is_verbal(self)
                - is_indeclinable(self)
                - feature_count(self)
                - has_features(self)
                - __str__(self)
        📄 morphological_repository.py
            🏗️ Classes:
              • class MorphologicalRepository:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - get_category(self, identifier)
                - categories(self)
                - contains_category(self, identifier)
                - get_rule(self, identifier)
                - rules(self)
                - nominal_rules(self)
                - verbal_rules(self)
                - indeclinable_rules(self)
                - category_count(self)
                - rule_count(self)
        📄 morphological_resolution_context.py
            🏗️ Classes:
              • class MorphologicalResolutionContext:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
        📄 morphological_resolution_kernel.py
            🏗️ Classes:
              • class MorphologicalResolutionKernel:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - resolution_strategy(self)
                - resolve(self, context)
                - __call__(self, context)
                - __str__(self)
        📄 morphological_resolution_result.py
            🏗️ Classes:
              • class MorphologicalResolutionResult:
                - has_analysis(self)
                - analysis(self)
                - analysis_count(self)
                - resolved(self)
                - unresolved(self)
                - is_unique(self)
                - is_ambiguous(self)
                - features(self)
                - word_form(self)
                - is_nominal(self)
                - is_verbal(self)
                - is_indeclinable(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
        📄 morphological_resolution_strategy.py
            🏗️ Classes:
              • class MorphologicalResolutionStrategy:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - resolve(self, context)
        📄 morphological_rule.py
            🏗️ Classes:
              • class MorphologicalRule:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - applies_to(self, word_form)
                - apply(self, word_form)
                - __str__(self)
        📄 morphological_rule_set.py
            🏗️ Classes:
              • class MorphologicalRuleSet:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_empty(self)
                - count(self)
                - add(self, rule)
                - apply(self, word_form)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 morphological_service.py
            🏗️ Classes:
              • class MorphologicalService:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - resolution_kernel(self)
                - resolve(self, context)
                - contribute(self, aggregate, context)
                - count(self)
                - __str__(self)
        📄 nominal_category.py
            🏗️ Classes:
              • class NominalCategory:
                - grammatical_domain(self)
                - is_nominal(self)
                - is_verbal(self)
        📄 nominal_morphological_rule.py
            🏗️ Classes:
              • class NominalMorphologicalRule:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - applies_to(self, word_form)
                - _guess_stem(self, text)
                - apply(self, word_form)
        📄 pada.py
            🏗️ Classes:
              • class Pada:
        📄 prayoga.py
            🏗️ Classes:
              • class Prayoga:
        📄 purusha.py
            🏗️ Classes:
              • class Purusha:
        📄 vacana.py
            🏗️ Classes:
              • class Vacana:
        📄 verbal_category.py
            🏗️ Classes:
              • class VerbalCategory:
                - grammatical_domain(self)
                - is_nominal(self)
                - is_verbal(self)
        📄 verbal_morphological_rule.py
            🏗️ Classes:
              • class VerbalMorphologicalRule:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - applies_to(self, word_form)
                - _guess_stem(self, text)
                - apply(self, word_form)
        📄 vibhakti.py
            🏗️ Classes:
              • class Vibhakti:
      📂 panini/
        📄 default_paninian_rule_matcher.py
            🏗️ Classes:
              • class DefaultPaninianRuleMatcher:
                - match(self, rule, context)
        📄 default_paninian_rule_repository.py
            🏗️ Classes:
              • class DefaultPaninianRuleRepository:
                - __init__(self, rules)
                - _bootstrap_rules(self)
                - all(self)
                - get_by_identifier(self, identifier)
                - get_by_sutra(self, sutra_number)
                - by_category(self, category)
                - with_rule(self, rule)
                - with_rules(self, rules)
                - rule_count(self)
                - is_empty(self)
                - is_not_empty(self)
        📄 paninian_conflict_resolution_pipeline.py
            🏗️ Classes:
              • class PaninianConflictResolutionPipeline:
                - resolve(self, conflict)
                - add_resolver(self, resolver)
                - resolver_count(self)
                - clear_history(self)
                - summary(self)
                - __len__(self)
                - __iter__(self)
                - __str__(self)
        📄 paninian_conflict_resolver.py
            🏗️ Classes:
              • class PaninianConflictResolver:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - supports(self, conflict)
                - resolve(self, conflict)
                - summary(self)
                - __str__(self)
        📄 paninian_default_conflict_pipeline.py
            🏗️ Classes:
              • class DefaultPaninianConflictPipeline:
                - __post_init__(self)
                - get_pipeline(self)
                - resolvers(self)
                - resolver_count(self)
                - summary(self)
                - __str__(self)
        📄 paninian_derivation_context.py
            🏗️ Classes:
              • class PaninianDerivationContext:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_active_rule(self)
                - has_tags(self)
                - tag_count(self)
                - has_diagnostics(self)
                - diagnostic_count(self)
                - with_subject(self, subject)
                - with_rule(self)
                - next_iteration(self)
                - summary(self)
                - __str__(self)
        📄 paninian_derivation_engine.py
            🏗️ Classes:
              • class PaninianDerivationEngine:
                - before_derivation(self, context)
                - after_derivation(self, context)
                - _record_step(self)
                - execute_rule(self, rule, context)
                - _match_rules(self, context)
                - derive(self, context)
                - execution_trace(self)
                - executed_rule_count(self)
                - clear_trace(self)
                - summary(self)
                - __str__(self)
        📄 paninian_derivation_pipeline.py
            🏗️ Classes:
              • class PaninianDerivationPipeline:
                - name(self)
                - display_name(self)
                - display_description(self)
                - execute(self, context)
                - add_stage(self, stage)
                - insert_stage(self, index, stage)
                - remove_stage(self, stage_type)
                - replace_stage(self, stage_type, replacement)
                - stages(self)
                - stage_count(self)
                - __len__(self)
                - __iter__(self)
                - __str__(self)
        📄 paninian_derivation_result.py
            🏗️ Classes:
              • class PaninianDerivationResult:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - surface_form(self)
                - current_form(self)
                - dhatu(self)
                - pratyaya(self)
                - stage_count(self)
                - has_trace(self)
                - trace_states(self)
                - applied_rules(self)
                - rule_count(self)
                - latest_rule(self)
                - has_diagnostics(self)
                - has_metadata(self)
                - metadata_value(self, key, default)
                - diagnostic_messages(self)
                - resolved(self)
                - state(self)
                - __str__(self)
        📄 paninian_derivation_stage.py
            🏗️ Classes:
              • class PaninianDerivationStage:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - stage_name(self)
                - stage_identifier(self)
                - is_applicable(self, context, state)
                - apply(self, context, state)
                - execute(self, context, state)
                - __str__(self)
        📄 paninian_derivation_state.py
            🏗️ Classes:
              • class PaninianDerivationState:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - rule_count(self)
                - latest_rule(self)
                - has_annotations(self)
                - with_form(self, new_form)
                - add_rule(self, rule_name)
                - annotate(self, key, value)
                - with_confidence(self, confidence)
                - initial(cls, context)
                - __str__(self)
        📄 paninian_derivation_trace.py
            🏗️ Classes:
              • class PaninianDerivationTrace:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - state_count(self)
                - is_empty(self)
                - is_not_empty(self)
                - first(self)
                - last(self)
                - current_state(self)
                - current_form(self)
                - add(self, state)
                - extend(self, states)
                - state_at(self, index)
                - stage_names(self)
                - surface_forms(self)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 paninian_execution_step.py
            🏗️ Classes:
              • class PaninianExecutionStep:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - operation(self)
                - behaviour(self)
                - candidate_count(self)
                - summary(self)
        📄 paninian_execution_trace.py
            🏗️ Classes:
              • class PaninianExecutionTrace:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - step_count(self)
                - is_empty(self)
                - first_step(self)
                - last_step(self)
                - append(self, step)
                - summary(self)
                - __len__(self)
                - __iter__(self)
                - __getitem__(self, index)
        📄 paninian_grammar.py
            🏗️ Classes:
              • class PaninianGrammar:
                - sutra_count(self)
                - implemented_sutras(self)
                - implementation_percentage(self)
                - summary(self)
                - __str__(self)
        📄 paninian_grammar_session.py
            🏗️ Classes:
              • class PaninianGrammarSession:
                - run(self)
                - executed_rule_count(self)
                - current_iteration(self)
                - summary(self)
                - reset(self, context)
                - __str__(self)
        📄 paninian_rule.py
            🏗️ Classes:
              • class PaninianRule:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - category(self)
                - operation(self)
                - behaviour(self)
                - rule_type(self)
                - priority(self)
                - source(self)
                - notes(self)
                - tags(self)
                - sutra(self)
                - sutra_number(self)
                - sutra_text(self)
                - transliteration(self)
                - translation(self)
                - adhyaya(self)
                - pada(self)
                - canonical_location(self)
                - is_enabled(self)
                - is_transformational(self)
                - is_phonological(self)
                - is_morphological(self)
                - has_operation(self)
                - supports(self, context)
                - validate(self, context)
                - before_apply(self, context)
                - apply(self, context)
                - after_apply(self, context, result)
                - explain(self)
                - trace(self)
                - __lt__(self, other)
                - __str__(self)
        📄 paninian_rule_behaviour.py
            🏗️ Classes:
              • class PaninianRuleBehaviour:
                - display_name(self)
                - is_transformative(self)
                - is_contextual(self)
                - is_descriptive(self)
        📄 paninian_rule_category.py
            🏗️ Classes:
              • class PaninianRuleCategory:
                - display_name(self)
                - is_meta_rule(self)
                - is_morphological(self)
                - is_phonological(self)
                - is_semantic(self)
                - __str__(self)
        📄 paninian_rule_collection.py
            🏗️ Classes:
              • class PaninianRuleCollection:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - count(self)
                - is_empty(self)
                - is_not_empty(self)
                - first(self)
                - last(self)
                - identifiers(self)
                - add(self, rule)
                - extend(self, rules)
                - sorted(self)
                - get_by_identifier(self, identifier)
                - get_by_sutra(self, sutra_number)
                - find_by_category(self, category)
                - enabled(self)
                - disabled(self)
                - remove_by_identifier(self, identifier)
                - __iter__(self)
                - __len__(self)
                - __contains__(self, identifier)
                - __getitem__(self, index)
                - __str__(self)
        📄 paninian_rule_condition.py
            🏗️ Classes:
              • class PaninianRuleCondition:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_enabled(self)
                - evaluate(self, context)
                - supports(self, context)
                - __lt__(self, other)
                - __str__(self)
        📄 paninian_rule_conflict.py
            🏗️ Classes:
              • class PaninianRuleConflict:
                - rule_count(self)
                - is_empty(self)
                - has_conflict(self)
                - summary(self)
        📄 paninian_rule_engine.py
            🏗️ Classes:
              • class PaninianRuleEngine:
                - display_name(self)
                - display_description(self)
                - execute(self)
                - execute_single_rule(self)
                - __str__(self)
        📄 paninian_rule_engine_context.py
            🏗️ Classes:
              • class PaninianRuleEngineContext:
                - display_name(self)
                - display_description(self)
                - current_form(self)
                - metadata(self)
                - stage(self)
                - __str__(self)
        📄 paninian_rule_engine_result.py
            🏗️ Classes:
              • class PaninianRuleEngineResult:
                - display_name(self)
                - display_description(self)
                - evaluated_rule_count(self)
                - matched_rule_count(self)
                - applied_rule_count(self)
                - changed(self)
                - has_matches(self)
                - has_applications(self)
                - __bool__(self)
                - __str__(self)
        📄 paninian_rule_match_result.py
            🏗️ Classes:
              • class PaninianRuleMatchResult:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_match(self)
                - is_not_match(self)
                - has_failures(self)
                - has_diagnostics(self)
                - matched_condition_count(self)
                - failed_condition_count(self)
                - diagnostic_count(self)
                - total_condition_count(self)
                - canonical_reference(self)
                - __lt__(self, other)
                - __bool__(self)
                - __str__(self)
        📄 paninian_rule_matcher.py
            🏗️ Classes:
              • class PaninianRuleMatcher:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - match(self, rule, context)
                - matches(self, rule, context)
                - supports(self, rule, context)
                - match_all(self, rules, context)
                - matching_rules(self, rules, context)
                - __str__(self)
        📄 paninian_rule_metadata.py
            🏗️ Classes:
              • class PaninianRuleMetadata:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_samjna(self)
                - is_paribhasha(self)
                - is_adhikara(self)
                - is_vidhi(self)
                - is_niyama(self)
                - is_atidesha(self)
                - has_operation(self)
                - is_transformational(self)
                - is_phonological(self)
                - is_morphological(self)
                - __str__(self)
        📄 paninian_rule_operation.py
            🏗️ Classes:
              • class PaninianRuleOperation:
                - display_name(self)
                - __str__(self)
        📄 paninian_rule_priority.py
            🏗️ Classes:
              • class PaninianRulePriority:
                - display_name(self)
                - is_default_priority(self)
                - is_exception_priority(self)
                - is_high_priority(self)
                - is_low_priority(self)
                - default(cls)
                - highest(cls)
                - lowest(cls)
                - __str__(self)
        📄 paninian_rule_repository.py
            🏗️ Classes:
              • class PaninianRuleRepository:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - all(self)
                - get_by_identifier(self, identifier)
                - get_by_sutra(self, sutra_number)
                - by_category(self, category)
                - enabled(self)
                - count(self)
                - contains(self, identifier)
                - __len__(self)
                - __iter__(self)
        📄 paninian_rule_set.py
            🏗️ Classes:
              • class PaninianRuleSet:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - rule_count(self)
                - is_empty(self)
                - enabled_rules(self)
                - applicable_rules(self, context)
                - apply(self, context)
                - add_rule(self, rule)
                - remove_rule(self, identifier)
                - __len__(self)
                - __iter__(self)
                - __str__(self)
        📄 paninian_rule_type.py
            🏗️ Classes:
              • class PaninianRuleType:
                - display_name(self)
                - is_executable(self)
                - is_annotation(self)
                - is_validation(self)
                - is_optional(self)
                - is_exception(self)
                - is_default(self)
                - __str__(self)
        📄 paninian_stage_collection.py
            🏗️ Classes:
              • class PaninianStageCollection:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - count(self)
                - is_empty(self)
                - is_not_empty(self)
                - first(self)
                - last(self)
                - stage_names(self)
                - add(self, stage)
                - extend(self, stages)
                - insert(self, index, stage)
                - remove(self, stage_name)
                - contains(self, stage_name)
                - find(self, stage_name)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __contains__(self, stage_name)
                - __str__(self)
        📄 paninian_sutra.py
            🏗️ Classes:
              • class PaninianSutra:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - canonical_location(self)
                - has_translation(self)
                - has_transliteration(self)
                - has_commentaries(self)
                - commentary_count(self)
                - __str__(self)
        📄 paninian_sutra_catalog.py
            🏗️ Classes:
              • class PaninianSutraCatalog:
                - load(self)
                - is_loaded(self)
                - index(self)
                - get(self, sutra_number)
                - by_adhyaya(self, adhyaya)
                - by_pada(self, pada)
                - by_category(self, category)
                - by_operation(self, operation)
                - by_behaviour(self, behaviour)
                - all(self)
                - count(self)
                - sutra_numbers(self)
                - __len__(self)
                - __iter__(self)
                - summary(self)
                - __str__(self)
        📄 paninian_sutra_index.py
            🏗️ Classes:
              • class PaninianSutraIndex:
                - __post_init__(self)
                - by_sutra_number(self, sutra_number)
                - by_adhyaya(self, adhyaya)
                - by_pada(self, pada)
                - by_category(self, category)
                - by_operation(self, operation)
                - by_behaviour(self, behaviour)
                - summary(self)
        📄 paninian_sutra_loader.py
            🏗️ Classes:
              • class PaninianSutraLoader:
                - discover_modules(self)
                - load_module(self, module_name)
                - load_all(self)
                - module_count(self)
                - implemented_sutras(self)
                - summary(self)
                - __len__(self)
                - __iter__(self)
                - __str__(self)
        📄 paninian_sutra_manifest.py
            🏗️ Classes:
              • class PaninianSutraManifest:
                - load_modules(self)
                - module_count(self)
                - implemented_sutra_numbers(self)
                - implementation_percentage(self)
                - contains(self, sutra_number)
                - summary(self)
                - __len__(self)
                - __iter__(self)
                - __contains__(self, item)
                - __str__(self)
        📄 paninian_sutra_registration.py
            🔹 Constants:
              • _REGISTRIES
            ⚙️ Functions:
              • get_registry(registry_name)
              • get_registered_class(sutra_number, registry_name)
              • clear_registry(registry_name)
              • register_paninian_sutra(sutra_number, registry_name)
            🏗️ Classes:
              • class PaninianSutraRegistration:
                - registry(self)
                - count(self)
                - sutra_numbers(self)
                - contains(self, sutra_number)
                - __len__(self)
                - __iter__(self)
                - __str__(self)
        📄 paninian_sutra_registry.py
            🏗️ Classes:
              • class PaninianSutraRegistry:
                - registry(self)
                - size(self)
                - is_empty(self)
                - sutra_numbers(self)
                - contains(self, sutra_number)
                - __contains__(self, sutra_number)
                - get_rule_class(self, sutra_number)
                - create(self, sutra_number)
                - rule_classes(self)
                - instances(self)
                - __iter__(self)
                - summary(self)
                - __len__(self)
                - __str__(self)
        📂 conflict_resolvers/
          📄 antaranga_resolver.py
              🏗️ Classes:
                • class AntarangaResolver:
                  - supports(self, conflict)
                  - _depth(rule)
                  - resolve(self, conflict)
                  - paribhasha(self)
                  - english(self)
                  - summary(self)
          📄 bahiranga_resolver.py
              🏗️ Classes:
                • class BahirangaResolver:
                  - supports(self, conflict)
                  - _depth(rule)
                  - resolve(self, conflict)
                  - paribhasha(self)
                  - english(self)
                  - summary(self)
          📄 vipratisedha_resolver.py
              🏗️ Classes:
                • class VipratisedhaResolver:
                  - supports(self, conflict)
                  - _ordering_key(rule)
                  - resolve(self, conflict)
                  - paribhasha(self)
                  - english(self)
                  - summary(self)
        📂 rules/
          📄 adesha_rule.py
              🏗️ Classes:
                • class AdeshaRule:
                  - __post_init__(self)
                  - is_adesha(self)
                  - performs_substitution(self)
                  - replaces_material(self)
                  - explain(self)
          📄 agama_rule.py
              🏗️ Classes:
                • class AgamaRule:
                  - __post_init__(self)
                  - is_agama(self)
                  - inserts_material(self)
                  - explain(self)
          📄 lopa_rule.py
              🏗️ Classes:
                • class LopaRule:
                  - __post_init__(self)
                  - is_lopa(self)
                  - deletes_material(self)
                  - performs_elision(self)
                  - explain(self)
          📄 samjna_rule.py
              🏗️ Classes:
                • class SamjnaRule:
                  - __post_init__(self)
                  - is_annotation_rule(self)
                  - establishes_technical_term(self)
                  - validate(self, context)
                  - apply(self, context)
          📄 sandhi_rule.py
              🏗️ Classes:
                • class SandhiRule:
                  - __post_init__(self)
                  - is_sandhi(self)
                  - is_phonological(self)
                  - performs_phonological_transformation(self)
                  - explain(self)
          📄 tripadi_rule.py
              🏗️ Classes:
                • class TripadiRule:
                  - __post_init__(self)
                  - is_tripadi(self)
                  - is_phonological(self)
                  - executes_after_sapadasaptadhyayi(self)
                  - explain(self)
          📄 vidhi_rule.py
              🏗️ Classes:
                • class VidhiRule:
                  - __post_init__(self)
                  - is_vidhi(self)
                  - is_operational(self)
                  - performs_transformation(self)
                  - explain(self)
          📂 sutras/
            📄 abstract_adhikara_sutra.py
                🏗️ Classes:
                  • class AbstractAdhikaraSutra:
                    - behaviour(self)
                    - supports(self, context)
                    - establish_scope(self, context)
                    - _execute_rule(self, context)
                    - scope_name(self)
                    - explain(self)
                    - trace(self)
                    - is_scope_rule(self)
            📄 abstract_atidesha_sutra.py
                🏗️ Classes:
                  • class AbstractAtideshaSutra:
                    - behaviour(self)
                    - extension_name(self)
                    - explain(self)
                    - trace(self)
                    - is_extension_rule(self)
            📄 abstract_niyama_sutra.py
                🏗️ Classes:
                  • class AbstractNiyamaSutra:
                    - behaviour(self)
                    - restriction_name(self)
                    - explain(self)
                    - trace(self)
            📄 abstract_paribhasha_sutra.py
                🏗️ Classes:
                  • class AbstractParibhashaSutra:
                    - supports(self, context)
                    - apply_meta_rule(self, context)
                    - _execute_rule(self, context)
                    - meta_rule_name(self)
                    - explain(self)
                    - trace(self)
            📄 abstract_samjna_sutra.py
                🏗️ Classes:
                  • class AbstractSamjnaSutra:
                    - supports(self, context)
                    - establish_designation(self, context)
                    - _execute_rule(self, context)
                    - designation_name(self)
                    - explain(self)
                    - trace(self)
            📄 abstract_sutra.py
                🏗️ Classes:
                  • class AbstractSutra:
                    - __init__(self)
                    - sutra(self)
                    - sutra_number(self)
                    - sutra_text(self)
                    - transliteration(self)
                    - translation(self)
                    - canonical_location(self)
                    - adhyaya(self)
                    - pada(self)
                    - supports(self, context)
                    - validate(self, context)
                    - before_apply(self, context)
                    - _execute_rule(self, context)
                    - after_apply(self, context, result)
                    - apply(self, context)
                    - explain(self)
                    - trace(self)
                    - display_name(self)
                    - display_text(self)
                    - display_description(self)
                    - __str__(self)
            📄 abstract_vidhi_sutra.py
                🏗️ Classes:
                  • class AbstractVidhiSutra:
                    - supports(self, context)
                    - perform_transformation(self, context)
                    - _execute_rule(self, context)
                    - transformation_name(self)
                    - explain(self)
                    - trace(self)
              📂 pada_1/
                📄 sutra_1_1_1_vrddhir_adaic.py
                    🏗️ Classes:
                      • class Sutra111VrddhirAdaic:
                        - __init__(self)
                        - supports(self, context)
                        - validate(self, context)
                        - apply(self, context)
        📂 stages/
          📄 agama_stage.py
              🏗️ Classes:
                • class AgamaStage:
                  - display_name(self)
                  - display_description(self)
                  - rule_set_name(self)
          📄 anga_processing_stage.py
              🏗️ Classes:
                • class AngaProcessingStage:
                  - display_name(self)
                  - display_description(self)
                  - rule_set_name(self)
          📄 default_paninian_stage_collection.py
              🏗️ Classes:
                • class DefaultPaninianStageCollection:
                  - __init__(self)
                  - create(cls)
          📄 dhatu_selection_stage.py
              🏗️ Classes:
                • class DhatuSelectionStage:
                  - display_name(self)
                  - display_description(self)
                  - rule_set_name(self)
          📄 final_form_stage.py
              🏗️ Classes:
                • class FinalFormStage:
                  - display_name(self)
                  - display_description(self)
                  - is_applicable(self, context, state)
                  - apply(self, context, state)
          📄 guna_vrddhi_stage.py
              🏗️ Classes:
                • class GunaVrddhiStage:
                  - display_name(self)
                  - display_description(self)
                  - rule_set_name(self)
          📄 it_samjna_stage.py
              🏗️ Classes:
                • class ItSamjnaStage:
                  - display_name(self)
                  - display_description(self)
                  - rule_set_name(self)
          📄 lopa_stage.py
              🏗️ Classes:
                • class LopaStage:
                  - display_name(self)
                  - display_description(self)
                  - rule_set_name(self)
          📄 paninian_rule_driven_stage.py
              🏗️ Classes:
                • class PaninianRuleDrivenStage:
                  - __init__(self)
                  - rule_set_name(self)
                  - is_applicable(self, context, state)
                  - apply(self, context, state)
          📄 pratyaya_selection_stage.py
              🏗️ Classes:
                • class PratyayaSelectionStage:
                  - display_name(self)
                  - display_description(self)
                  - rule_set_name(self)
          📄 sandhi_stage.py
              🏗️ Classes:
                • class SandhiStage:
                  - display_name(self)
                  - display_description(self)
                  - rule_set_name(self)
          📄 substitution_stage.py
              🏗️ Classes:
                • class SubstitutionStage:
                  - display_name(self)
                  - display_description(self)
                  - rule_set_name(self)
          📄 tripadi_stage.py
              🏗️ Classes:
                • class TripadiStage:
                  - display_name(self)
                  - display_description(self)
                  - rule_set_name(self)
      📂 phonology/
        📄 anusvara.py
            🏗️ Classes:
              • class Anusvara:
                - display_name(self)
        📄 consonant.py
            🏗️ Classes:
              • class Consonant:
                - is_consonant(self)
                - display_name(self)
        📄 jihvamuliya.py
            🏗️ Classes:
              • class Jihvamuliya:
                - display_name(self)
                - display_text(self)
                - display_description(self)
        📄 non_alphabetic_ayogavaha_phoneme.py
            🏗️ Classes:
              • class NonAlphabeticAyogavahaPhoneme:
                - is_non_alphabetic(self)
                - is_ayogavaha(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
        📄 phoneme.py
            🏗️ Classes:
              • class Phoneme:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_property(self, property)
                - has_any_property(self, *properties)
                - has_all_properties(self, *properties)
                - property_count(self)
                - is_vowel(self)
                - is_consonant(self)
                - is_non_alphabetic(self)
                - is_ayogavaha(self)
                - __str__(self)
        📄 phoneme_class.py
            🔹 Constants:
              • AC
              • HAL
              • ANTASTHA
              • USHMAN
              • AYOGAVAHA
            🏗️ Classes:
              • class PhonemeClass:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
        📄 phoneme_classifier.py
            🏗️ Classes:
              • class PhonemeClassifier:
                - is_ac(phoneme)
                - is_hal(phoneme)
                - is_ayogavaha(phoneme)
                - is_visarga(phoneme)
                - is_anusvara(phoneme)
                - is_jihvamuliya(phoneme)
                - is_upadhmaniya(phoneme)
                - is_short_vowel(phoneme)
                - is_long_vowel(phoneme)
                - is_kanthya(phoneme)
                - is_osthya(phoneme)
        📄 phoneme_factory.py
            🏗️ Classes:
              • class PhonemeFactory:
                - create_phoneme(specification)
                - create_phonemes(cls, specification)
                - create_inventory(cls, specification)
                - create_default_inventory(cls)
        📄 phoneme_inventory.py
            🏗️ Classes:
              • class PhonemeInventory:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - count(self)
                - is_empty(self)
                - get(self, symbol)
                - contains(self, symbol)
                - symbols(self)
                - values(self)
                - __len__(self)
                - __iter__(self)
                - __contains__(self, symbol)
                - __str__(self)
        📄 phoneme_property.py
            🔹 Constants:
              • HRASVA
              • DIRGHA
              • PLUTA
              • KANTHYA
              • TALAVYA
              • MURDHANYA
              • DANTYA
              • OSTHYA
              • GHOSHA
              • AGHOSHA
              • ALPAPRANA
              • MAHAPRANA
              • NASIKA
              • SEMIVOWEL
              • SIBILANT
              • AYOGAVAHA
              • JIHVAMULIYA
              • UPADHMANIYA
            🏗️ Classes:
              • class PhonemeProperty:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
        📄 phoneme_specification.py
            🔹 Constants:
              • CANONICAL_PHONEME_SPECIFICATION
        📄 phonology.py
            🔹 Constants:
              • DEFAULT_PHONOLOGY
            🏗️ Classes:
              • class Phonology:
                - __init__(self, inventory, classifier)
                - inventory(self)
                - classifier(self)
                - phoneme(self, symbol)
                - contains(self, symbol)
                - is_ac(self, symbol)
                - is_hal(self, symbol)
                - is_ayogavaha(self, symbol)
                - is_visarga(self, symbol)
                - is_anusvara(self, symbol)
                - is_jihvamuliya(self, symbol)
                - is_upadhmaniya(self, symbol)
                - is_short_vowel(self, symbol)
                - is_long_vowel(self, symbol)
                - __str__(self)
        📄 upadhmaniya.py
            🏗️ Classes:
              • class Upadhmaniya:
                - display_name(self)
                - display_text(self)
                - display_description(self)
        📄 visarga.py
            🏗️ Classes:
              • class Visarga:
                - display_name(self)
        📄 vowel.py
            🏗️ Classes:
              • class Vowel:
                - is_vowel(self)
                - display_name(self)
      📂 pipeline/
        📄 default_alankara_pipeline.py
            🏗️ Classes:
              • class DefaultAlankaraPipeline:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - before_execute(self, context)
                - after_execute(self, context, result)
                - step_names(self)
                - is_configured(self)
                - execute_alankara(self, context)
        📄 default_chandas_pipeline.py
            🏗️ Classes:
              • class DefaultChandasPipeline:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - before_execute(self, context)
                - after_execute(self, context, result)
                - step_names(self)
                - is_configured(self)
                - execute_chandas(self, context)
        📄 default_derivation_pipeline.py
            🏗️ Classes:
              • class DefaultDerivationPipeline:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - before_execute(self, context)
                - after_execute(self, context, result)
                - step_names(self)
                - is_configured(self)
                - execute_derivation(self, context)
        📄 default_knowledge_graph_pipeline.py
            🏗️ Classes:
              • class DefaultKnowledgeGraphPipeline:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - before_execute(self, context)
                - after_execute(self, context, result)
                - step_names(self)
                - is_configured(self)
                - execute_graph(self, context)
        📄 default_semantic_pipeline.py
            🏗️ Classes:
              • class DefaultSemanticPipeline:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - before_execute(self, context)
                - after_execute(self, context, result)
                - step_names(self)
                - is_configured(self)
                - execute_semantic(self, context)
        📄 default_vakya_pipeline.py
            🏗️ Classes:
              • class DefaultVakyaPipeline:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - before_execute(self, context)
                - after_execute(self, context, result)
                - step_names(self)
                - is_configured(self)
                - execute_vakya(self, context)
        📄 derivation_pipeline_context.py
            🏗️ Classes:
              • class DerivationPipelineContext:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_subject(self)
                - has_dhatu(self)
                - has_pratyaya(self)
                - has_metadata(self)
                - metadata_keys(self)
                - get(self, key, default)
                - with_metadata(self, **metadata)
                - __str__(self)
        📄 derivation_pipeline_result.py
            🏗️ Classes:
              • class DerivationPipelineResult:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - resolved(self)
                - has_trace(self)
                - trace_step_count(self)
                - has_diagnostics(self)
                - diagnostic_count(self)
                - result(self)
                - __str__(self)
        📄 derivation_pipeline_step.py
            🏗️ Classes:
              • class DerivationPipelineStep:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - execute(self, context, value)
                - is_enabled(self)
                - is_disabled(self)
                - has_metadata(self)
                - get(self, key, default)
                - with_priority(self, priority)
                - with_enabled(self, enabled)
                - __lt__(self, other)
                - __str__(self)
        📄 derivation_pipeline_trace.py
            🏗️ Classes:
              • class DerivationPipelineTraceEntry:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_input(self)
                - has_output(self)
                - has_diagnostics(self)
                - diagnostic_count(self)
                - kernel(self)
              • class DerivationPipelineTrace:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - count(self)
                - is_empty(self)
                - is_not_empty(self)
                - first(self)
                - last(self)
                - successful_steps(self)
                - failed_steps(self)
                - has_failures(self)
                - kernels(self)
                - add(self, entry)
                - extend(self, entries)
                - by_kernel(self, kernel)
                - __iter__(self)
                - __len__(self)
                - __str__(self)
      📂 pratyaya/
        📄 default_pratyaya_repository.py
            🏗️ Classes:
              • class DefaultPratyayaRepository:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - get(self, identifier)
                - find_by_category(self, category)
                - find_by_surface(self, surface)
                - search(self, query)
                - all(self)
                - contains(self, identifier)
                - count(self)
        📄 default_pratyaya_resolver.py
            🏗️ Classes:
              • class DefaultPratyayaResolver:
                - __init__(self, strategy)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, context)
        📄 default_pratyaya_rule_set.py
            🔹 Constants:
              • DEFAULT_PRATYAYA_RULES
            ⚙️ Functions:
              • default_pratyaya_rule_set()
        📄 default_pratyaya_strategy.py
            🏗️ Classes:
              • class DefaultPratyayaStrategy:
                - __init__(self, rule_set, repository, collection)
                - rule_set(self)
                - repository(self)
                - collection(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - _canonical_collection(self)
                - _match_pratyaya(self, surface, canonical)
                - _to_analysis_collection(self, context, candidates)
                - analyze(self, context)
        📄 pratyaya_analysis.py
            🏗️ Classes:
              • class PratyayaAnalysis:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_rule(self)
                - has_notes(self)
                - is_confident(self)
                - __str__(self)
        📄 pratyaya_analysis_collection.py
            🏗️ Classes:
              • class PratyayaAnalysisCollection:
                - count(self)
                - is_empty(self)
                - has_analyses(self)
                - first(self)
                - best(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - add(self, analysis)
                - extend(self, other)
                - __len__(self)
                - __iter__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 pratyaya_context.py
            🏗️ Classes:
              • class PratyayaContext:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_source(self)
                - has_metadata(self)
                - metadata_count(self)
                - recursive(self)
                - multiple_analyses_enabled(self)
                - get(self, key, default)
                - __str__(self)
        📄 pratyaya_diagnostic.py
            🏗️ Classes:
              • class PratyayaDiagnostic:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_info(self)
                - is_warning(self)
                - is_error(self)
                - has_rule(self)
                - has_location(self)
                - __str__(self)
        📄 pratyaya_factory.py
            🏗️ Classes:
              • class Pratyaya:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_category(self)
                - has_notes(self)
                - __str__(self)
              • class PratyayaCollection:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - count(self)
                - is_empty(self)
                - first(self)
                - add(self, pratyaya)
                - extend(self, other)
                - get_by_identifier(self, identifier)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
              • class PratyayaFactory:
                - create_pratyaya(specification)
                - create_pratyayas(cls, specification)
                - create_collection(cls, specification)
                - create_default_collection(cls)
        📄 pratyaya_repository.py
            🏗️ Classes:
              • class PratyayaRepository:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - get(self, identifier)
                - find_by_category(self, category)
                - find_by_surface(self, surface)
                - search(self, query)
                - all(self)
                - contains(self, identifier)
                - count(self)
        📄 pratyaya_resolver.py
            🏗️ Classes:
              • class PratyayaResolver:
                - __init__(self, strategy)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - strategy(self)
                - analyze(self, context)
                - __str__(self)
        📄 pratyaya_result.py
            🏗️ Classes:
              • class PratyayaResult:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - subject(self)
                - source(self)
                - language(self)
                - script(self)
                - result(self)
                - analysis_count(self)
                - has_analyses(self)
                - first_analysis(self)
                - has_diagnostics(self)
                - diagnostic_count(self)
                - has_errors(self)
                - has_warnings(self)
                - first_diagnostic(self)
                - resolved(self)
                - unresolved(self)
                - is_confident(self)
                - best_analysis(self)
                - __str__(self)
        📄 pratyaya_rule.py
            🏗️ Classes:
              • class PratyayaRule:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - applies_to(self, context)
                - apply(self, context)
                - __str__(self)
              • class KnownPratyayaRule:
                - display_name(self)
                - display_description(self)
                - _extract_text(self, context)
                - _hinted(self, context)
                - applies_to(self, context)
                - apply(self, context)
              • class AffixHintRule:
                - display_name(self)
                - display_description(self)
                - applies_to(self, context)
                - apply(self, context)
        📄 pratyaya_rule_set.py
            🏗️ Classes:
              • class PratyayaRuleSet:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_empty(self)
                - count(self)
                - add(self, rule)
                - apply(self, context)
                - __len__(self)
                - __iter__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 pratyaya_specification.py
            🔹 Constants:
              • CANONICAL_PRATYAYA_SPECIFICATION
            🏗️ Classes:
              • class PratyayaSpecification:
        📄 pratyaya_strategy.py
            🏗️ Classes:
              • class PratyayaStrategy:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, context)
                - __str__(self)
        📄 specific_pratyaya_rules.py
            🏗️ Classes:
              • class _ExactPratyayaRule:
                - _text(self, context)
                - _hinted(self, context)
                - applies_to(self, context)
                - apply(self, context)
              • class KtaPratyayaRule:
                - display_name(self)
                - display_description(self)
              • class KtvaPratyayaRule:
                - display_name(self)
                - display_description(self)
              • class TumunPratyayaRule:
                - display_name(self)
                - display_description(self)
              • class LyapPratyayaRule:
                - display_name(self)
                - display_description(self)
              • class ShatrPratyayaRule:
                - display_name(self)
                - display_description(self)
              • class ShanacPratyayaRule:
                - display_name(self)
                - display_description(self)
              • class NvulPratyayaRule:
                - display_name(self)
                - display_description(self)
              • class AniyaPratyayaRule:
                - display_name(self)
                - display_description(self)
      📂 reader/
        📄 chapter_position.py
            🏗️ Classes:
              • class ChapterPosition:
                - __post_init__(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
        📄 chapter_view.py
            🏗️ Classes:
              • class ChapterView:
                - display_name(self)
                - display_description(self)
                - sloka_count(self)
                - is_empty(self)
                - sloka(self, sloka_id)
                - contains(self, position)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
        📄 default_reader_repository.py
            🔹 Constants:
              • T
            🏗️ Classes:
              • class DefaultReaderRepository:
                - __post_init__(self)
                - document(self)
                - get_document(self, document_id)
                - get_chapter(self, chapter_id)
                - get_chapters(self)
                - get_chapter_slokas(self, chapter_id)
                - next_chapter(self, chapter_id)
                - previous_chapter(self, chapter_id)
                - get_sloka(self, sloka_id)
                - get_slokas(self)
                - get_sloka_words(self, sloka_id)
                - next_sloka(self, sloka_id)
                - previous_sloka(self, sloka_id)
                - get_word(self, word_id)
                - get_words(self)
                - next_word(self, word_id)
                - previous_word(self, word_id)
                - resolve_position(self, position)
                - _next_in_mapping(mapping, identifier)
                - _previous_in_mapping(mapping, identifier)
                - _build_reader_document(self)
                - _build_chapter(self, document, section)
                - _verse_text(self, verse)
                - _build_sloka(self, document, section, verse)
                - _extract_words(self, document, section, verse)
                - _build_word(self, document, section, verse, token)
                - _purana_identifier(self)
                - _corpus_title(self)
                - _title_from_metadata(metadata, fallback)
                - _metadata_dict(node)
                - chapter_count(self)
                - sloka_count(self)
                - word_count(self)
                - __len__(self)
        📄 reader_context.py
            🏗️ Classes:
              • class ReaderContext:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_source(self)
                - has_language(self)
                - has_script(self)
                - has_metadata(self)
                - get_metadata(self, key, default)
                - __str__(self)
        📄 reader_controller.py
            🏗️ Classes:
              • class ReaderController:
                - open(cls, engine, position)
                - engine(self)
                - position(self)
                - current_position(self)
                - has_position(self)
                - result(self)
                - current_result(self)
                - has_result(self)
                - succeeded(self)
                - can_go_back(self)
                - can_go_forward(self)
                - history_count(self)
                - open_position(self, position)
                - set_position(self, position)
                - resolve(self)
                - next(self)
                - previous(self)
                - back(self)
                - forward(self)
                - move_next(self)
                - move_previous(self)
                - clear_history(self)
                - document(self, document_id)
                - chapter(self, chapter_id)
                - sloka(self, sloka_id)
                - word(self, word_id)
                - resolve_position(self, position)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
        📄 reader_document.py
            🏗️ Classes:
              • class ReaderDocument:
                - display_name(self)
                - display_description(self)
                - chapter_count(self)
                - is_empty(self)
                - chapter(self, chapter_id)
                - contains(self, position)
                - __iter__(self)
                - __len__(self)
        📄 reader_engine.py
            🏗️ Classes:
              • class ReaderEngine:
                - document(self, document_id)
                - chapter(self, chapter_id)
                - next_chapter(self, position)
                - previous_chapter(self, position)
                - sloka(self, sloka_id)
                - next_sloka(self, position)
                - previous_sloka(self, position)
                - word(self, word_id)
                - next_word(self, position)
                - previous_word(self, position)
                - resolve(self, position)
                - move_next(self, position)
                - move_previous(self, position)
        📄 reader_interaction.py
            🏗️ Classes:
              • class ReaderHoverContext:
                - purana_id(self)
                - chapter_id(self)
                - sloka_id(self)
                - word_id(self)
                - level(self)
                - canonical_id(self)
                - from_position(cls, position)
                - to_position(self)
                - __str__(self)
              • class ReaderInteraction:
                - hover(position)
                - select(position)
        📄 reader_navigator.py
            🏗️ Classes:
              • class ReaderNavigator:
                - next_chapter(self, position)
                - previous_chapter(self, position)
                - next_sloka(self, position)
                - previous_sloka(self, position)
                - next_word(self, position)
                - previous_word(self, position)
                - _chapter_position(self, chapter, current)
                - _sloka_position(self, sloka, current)
                - _word_position(self, word, current)
                - _require_chapter_id(position)
                - _require_sloka_id(position)
                - _require_word_id(position)
        📄 reader_node.py
            🏗️ Classes:
              • class ReaderNode:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_parent(self)
                - has_children(self)
                - child_count(self)
                - is_root(self)
                - is_leaf(self)
                - has_metadata(self)
                - metadata_value(self, key, default)
                - sort_key(self)
                - __len__(self)
                - __iter__(self)
                - __contains__(self, identifier)
                - __str__(self)
        📄 reader_position.py
            🏗️ Classes:
              • class ReaderPosition:
                - __post_init__(self)
                - level(self)
                - is_purana(self)
                - is_chapter(self)
                - is_sloka(self)
                - is_word(self)
                - canonical_id(self)
                - identifier(self)
                - chapter_position(self)
                - sloka_position(self)
                - word_position(self)
                - to_dict(self)
                - __str__(self)
                - __repr__(self)
        📄 reader_position_factory.py
            🏗️ Classes:
              • class ReaderPositionFactory:
                - _require_id(value, name)
                - purana(cls)
                - chapter(cls)
                - sloka(cls)
                - word(cls)
        📄 reader_repository.py
            🏗️ Classes:
              • class ReaderRepository:
                - get_document(self, document_id)
                - get_chapter(self, chapter_id)
                - get_sloka(self, sloka_id)
                - get_word(self, word_id)
                - next_chapter(self, chapter_id)
                - previous_chapter(self, chapter_id)
                - next_sloka(self, sloka_id)
                - previous_sloka(self, sloka_id)
                - next_word(self, word_id)
                - previous_word(self, word_id)
        📄 reader_result.py
            🏗️ Classes:
              • class ReaderResult:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - lexical_available(self)
                - morphology_available(self)
                - sandhi_available(self)
                - samasa_available(self)
                - semantic_available(self)
                - pragmatics_available(self)
                - commentary_available(self)
                - completed_stage_count(self)
                - total_stage_count(self)
                - completion_ratio(self)
                - is_complete(self)
                - has_cross_references(self)
                - cross_reference_count(self)
                - has_canonical_sources(self)
                - canonical_source_count(self)
                - has_metadata(self)
                - get_metadata(self, key, default)
                - __str__(self)
        📄 reader_selection_context.py
            🏗️ Classes:
              • class ReaderSelectionContext:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - purana_id(self)
                - chapter_id(self)
                - sloka_id(self)
                - word_id(self)
                - level(self)
                - canonical_id(self)
                - identifier(self)
                - is_purana(self)
                - is_chapter(self)
                - is_sloka(self)
                - is_word(self)
                - has_chapter(self)
                - has_sloka(self)
                - has_word(self)
                - from_position(cls, position)
                - to_position(self)
                - __str__(self)
        📄 reader_service_registry.py
            🏗️ Classes:
              • class ReaderServiceRegistry:
                - __post_init__(self)
                - repository(self)
                - navigator(self)
        📄 reader_session.py
            🏗️ Classes:
              • class ReaderSession:
                - __post_init__(self)
                - current_position(self)
                - has_position(self)
                - result(self)
                - current_result(self)
                - has_result(self)
                - succeeded(self)
                - can_go_back(self)
                - can_go_forward(self)
                - history_count(self)
                - open(self, position)
                - set_position(self, position)
                - resolve(self)
                - _prepare_structural_history(self, result)
                - next(self)
                - previous(self)
                - move_next(self)
                - move_previous(self)
                - _synchronize_manual_history(self)
                - back(self)
                - forward(self)
                - clear_history(self)
                - _copy_history(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
        📄 reader_session_history.py
            🏗️ Classes:
              • class ReaderSessionHistory:
                - current(self)
                - position(self)
                - has_current(self)
                - can_go_back(self)
                - can_back(self)
                - can_go_forward(self)
                - can_forward(self)
                - back_count(self)
                - forward_count(self)
                - history_count(self)
                - record(self, position)
                - push(self, position)
                - back(self)
                - forward(self)
                - previous(self)
                - next(self)
                - clear(self)
                - clear_forward(self)
                - is_empty(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
        📄 reader_view.py
            🏗️ Classes:
              • class ReaderView:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - corpus_id(self)
                - purana_id(self)
                - chapter_id(self)
                - sloka_id(self)
                - word_id(self)
                - has_metadata(self)
                - get_metadata(self, key, default)
                - __str__(self)
        📄 reader_workspace.py
            🏗️ Classes:
              • class ReaderWorkspace:
                - open(cls, engine, position)
                - session(self)
                - engine(self)
                - position(self)
                - current_position(self)
                - selection(self)
                - result(self)
                - current_result(self)
                - has_position(self)
                - has_result(self)
                - succeeded(self)
                - can_go_back(self)
                - can_go_forward(self)
                - history_count(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - __str__(self)
        📄 sloka_position.py
            🏗️ Classes:
              • class SlokaPosition:
                - __post_init__(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
        📄 sloka_view.py
            🏗️ Classes:
              • class SlokaView:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - word_count(self)
                - is_empty(self)
                - word(self, word_id)
                - contains(self, position)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
        📄 word_position.py
            🏗️ Classes:
              • class WordPosition:
                - display_name(self)
                - display_text(self)
                - display_description(self)
        📄 word_view.py
            🏗️ Classes:
              • class WordView:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_transliteration(self)
                - has_normalized(self)
                - lexical_key(self)
      📂 resolution/
        📄 default_resolution_pipeline.py
            ⚙️ Functions:
              • default_resolution_pipeline(services)
        📄 lexical_resolution_stage.py
            🏗️ Classes:
              • class LexicalResolutionStage:
                - name(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - execute(self, context)
        📄 morphology_resolution_stage.py
            🏗️ Classes:
              • class MorphologyResolutionStage:
                - name(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - execute(self, context)
        📄 resolution_context.py
            🏗️ Classes:
              • class ResolutionContext:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_source(self)
                - has_language(self)
                - has_script(self)
                - has_metadata(self)
                - get_metadata(self, key, default)
                - __str__(self)
        📄 resolution_contributor.py
            🏗️ Classes:
              • class ResolutionContributor:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - contribute(self, aggregate, context)
                - __str__(self)
        📄 resolution_diagnostic.py
            🏗️ Classes:
              • class ResolutionDiagnostic:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_information(self)
                - is_warning(self)
                - is_error(self)
                - is_fatal(self)
                - has_source(self)
                - __str__(self)
        📄 resolution_pipeline.py
            🏗️ Classes:
              • class ResolutionPipeline:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - stage_count(self)
                - is_empty(self)
                - execute(self, context)
                - __iter__(self)
                - __len__(self)
                - __str__(self)
        📄 resolution_result.py
            🏗️ Classes:
              • class ResolutionResult:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - subject(self)
                - has_lexical(self)
                - has_morphology(self)
                - has_sandhi(self)
                - has_samasa(self)
                - has_semantic(self)
                - fully_resolved(self)
                - has_diagnostics(self)
                - diagnostic_count(self)
                - with_lexical(self, result)
                - with_morphology(self, result)
                - with_sandhi(self, result)
                - with_samasa(self, result)
                - with_semantic(self, result)
                - __str__(self)
        📄 resolution_stage.py
            🏗️ Classes:
              • class ResolutionStage:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - execute(self, aggregate)
                - context_type(self)
                - __str__(self)
        📄 resolution_state.py
            🏗️ Classes:
              • class ResolutionState:
                - subject(self)
                - identifier(self)
                - has_lexical(self)
                - has_morphology(self)
                - has_sandhi(self)
                - has_samasa(self)
                - has_semantics(self)
                - stage_count(self)
                - has_failures(self)
                - succeeded(self)
                - mark_completed(self, stage_name)
                - mark_failed(self, stage_name)
                - add_diagnostic(self, diagnostic)
                - set_metadata(self, key, value)
                - get_metadata(self, key, default)
        📄 resolution_strategy.py
            🏗️ Classes:
              • class ResolutionStrategy:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - resolve(self, context)
                - __str__(self)
        📄 resolver.py
            🏗️ Classes:
              • class Resolver:
                - __init__(self, strategy)
                - strategy(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - resolve(self, context)
                - __setattr__(self, name, value)
                - __str__(self)
        📄 samasa_resolution_stage.py
            🏗️ Classes:
              • class SamasaResolutionStage:
                - name(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - execute(self, context)
        📄 sandhi_resolution_stage.py
            🏗️ Classes:
              • class SandhiResolutionStage:
                - name(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - execute(self, context)
        📄 semantic_resolution_stage.py
            🏗️ Classes:
              • class SemanticResolutionStage:
                - name(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - execute(self, context)
      📂 samasa/
        📄 avyayibhava_rule.py
            🏗️ Classes:
              • class AvyayibhavaRule:
                - display_name(self)
                - display_description(self)
                - _extract_text(self, context)
                - _hinted(self, context)
                - applies_to(self, context)
                - apply(self, context)
        📄 bahuvrihi_rule.py
            🏗️ Classes:
              • class BahuvrihiRule:
                - display_name(self)
                - display_description(self)
                - _extract_text(self, context)
                - _hinted(self, context)
                - applies_to(self, context)
                - apply(self, context)
        📄 default_samasa_repository.py
            🏗️ Classes:
              • class DefaultSamasaRepository:
                - get(self, identifier)
                - search(self, query)
                - all(self)
                - count(self)
        📄 default_samasa_resolution_kernel.py
            🏗️ Classes:
              • class DefaultSamasaResolutionKernel:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - resolution_strategy(self)
                - kernel(self)
                - build_context(self, context)
                - resolve(self, context)
                - __call__(self, context)
                - __str__(self)
        📄 default_samasa_resolver.py
            🏗️ Classes:
              • class DefaultSamasaResolver:
                - __init__(self, strategy)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, context)
        📄 default_samasa_rule_set.py
            🔹 Constants:
              • DEFAULT_SAMASA_RULES
            ⚙️ Functions:
              • default_samasa_rule_set()
        📄 default_samasa_service.py
            🏗️ Classes:
              • class DefaultSamasaService:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - repository(self)
                - get_rule(self, identifier)
                - search_rules(self, query)
                - all_rules(self)
                - rule_count(self)
        📄 default_samasa_strategy.py
            🏗️ Classes:
              • class DefaultSamasaStrategy:
                - __init__(self, rule_set)
                - rule_set(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, context)
        📄 dvandva_rule.py
            🏗️ Classes:
              • class DvandvaRule:
                - display_name(self)
                - display_description(self)
                - _extract_text(self, context)
                - _hinted(self, context)
                - applies_to(self, context)
                - apply(self, context)
        📄 dvigu_rule.py
            🏗️ Classes:
              • class DviguRule:
                - display_name(self)
                - display_description(self)
                - _extract_text(self, context)
                - _hinted(self, context)
                - applies_to(self, context)
                - apply(self, context)
        📄 karmadharaya_rule.py
            🏗️ Classes:
              • class KarmadharayaRule:
                - display_name(self)
                - display_description(self)
                - _extract_text(self, context)
                - _hinted(self, context)
                - applies_to(self, context)
                - apply(self, context)
        📄 samasa_analysis.py
            🏗️ Classes:
              • class SamasaAnalysis:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_outputs(self)
                - output_count(self)
                - is_confident(self)
                - has_notes(self)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 samasa_analysis_collection.py
            🏗️ Classes:
              • class SamasaAnalysisCollection:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_empty(self)
                - count(self)
                - has_analyses(self)
                - first(self)
                - last(self)
                - add(self, analysis)
                - extend(self, other)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 samasa_context.py
            🏗️ Classes:
              • class SamasaContext:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_source(self)
                - has_metadata(self)
                - metadata_count(self)
                - recursive(self)
                - multiple_analyses_enabled(self)
                - get(self, key, default)
                - __str__(self)
        📄 samasa_diagnostic.py
            🏗️ Classes:
              • class SamasaDiagnostic:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_info(self)
                - is_warning(self)
                - is_error(self)
                - has_rule(self)
                - has_location(self)
                - __str__(self)
        📄 samasa_repository.py
            🏗️ Classes:
              • class SamasaRepository:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - get(self, identifier)
                - search(self, query)
                - all(self)
                - count(self)
        📄 samasa_resolution_kernel.py
            🏗️ Classes:
              • class SamasaResolutionKernel:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - resolution_strategy(self)
                - resolve(self, context)
                - _to_resolution_result(self, result)
                - __call__(self, context)
                - __str__(self)
        📄 samasa_resolution_result.py
            🏗️ Classes:
              • class SamasaResolutionResult:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - result(self)
                - has_analyses(self)
                - analysis_count(self)
                - succeeded(self)
                - __str__(self)
        📄 samasa_resolver.py
            🏗️ Classes:
              • class SamasaResolver:
                - __init__(self, strategy)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - strategy(self)
                - analyze(self, context)
                - __str__(self)
        📄 samasa_result.py
            🏗️ Classes:
              • class SamasaResult:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - subject(self)
                - source(self)
                - language(self)
                - script(self)
                - has_diagnostics(self)
                - diagnostic_count(self)
                - has_errors(self)
                - has_warnings(self)
                - first_diagnostic(self)
                - resolved(self)
                - unresolved(self)
                - is_confident(self)
                - has_analyses(self)
                - analysis_count(self)
                - first_analysis(self)
                - result(self)
                - __str__(self)
        📄 samasa_rule.py
            🏗️ Classes:
              • class SamasaRule:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - applies_to(self, context)
                - apply(self, context)
                - __str__(self)
        📄 samasa_rule_set.py
            🏗️ Classes:
              • class SamasaRuleSet:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_empty(self)
                - count(self)
                - add(self, rule)
                - apply(self, context)
                - __len__(self)
                - __iter__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 samasa_service.py
            🏗️ Classes:
              • class SamasaService:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - resolution_kernel(self)
                - resolve(self, context)
                - contribute(self, aggregate, context)
                - count(self)
                - __str__(self)
        📄 samasa_strategy.py
            🏗️ Classes:
              • class SamasaStrategy:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, context)
                - __str__(self)
        📄 tatpurusha_rule.py
            🏗️ Classes:
              • class TatpurushaRule:
                - display_name(self)
                - display_description(self)
                - _extract_text(self, context)
                - _hinted(self, context)
                - applies_to(self, context)
                - apply(self, context)
      📂 sandhi/
        📄 default_sandhi_repository.py
            🏗️ Classes:
              • class DefaultSandhiRepository:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - get(self, identifier)
                - contains(self, identifier)
                - search(self, query)
                - all(self)
                - count(self)
                - __str__(self)
        📄 default_sandhi_resolution_kernel.py
            🏗️ Classes:
              • class DefaultSandhiResolutionKernel:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - resolution_strategy(self)
                - kernel(self)
                - resolve(self, context)
                - __call__(self, context)
                - __str__(self)
        📄 default_sandhi_resolver.py
            🏗️ Classes:
              • class DefaultSandhiResolver:
                - __init__(self, strategy)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - resolve(self, context)
        📄 default_sandhi_rule_set.py
            🔹 Constants:
              • DEFAULT_SANDHI_RULES
            ⚙️ Functions:
              • default_sandhi_rule_set()
        📄 default_sandhi_service.py
            ⚙️ Functions:
              • _default_sandhi_repository()
            🏗️ Classes:
              • class DefaultSandhiService:
                - __init__(self, repository)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - get_rule(self, identifier)
                - search_rules(self, query)
                - all_rules(self)
                - rule_count(self)
                - __str__(self)
        📄 default_sandhi_strategy.py
            🏗️ Classes:
              • class DefaultSandhiStrategy:
                - __init__(self, rule_set)
                - rule_set(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - resolve(self, context)
        📄 guna_sandhi_rule.py
            🏗️ Classes:
              • class GunaSandhiRule:
                - display_name(self)
                - display_description(self)
                - _extract_words(self, context)
                - applies_to(self, context)
                - apply(self, context)
        📄 jastva_rule.py
            🏗️ Classes:
              • class JastvaRule:
                - display_name(self)
                - display_description(self)
                - _extract_words(self, context)
                - applies_to(self, context)
                - apply(self, context)
        📄 jihvamuliya_rule.py
            🏗️ Classes:
              • class JihvamuliyaRule:
                - display_name(self)
                - display_description(self)
                - _extract_words(self, context)
                - applies_to(self, context)
                - apply(self, context)
        📄 sandhi_analysis.py
            🏗️ Classes:
              • class SandhiAnalysis:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_outputs(self)
                - output_count(self)
                - is_confident(self)
                - has_notes(self)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 sandhi_analysis_collection.py
            🏗️ Classes:
              • class SandhiAnalysisCollection:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_empty(self)
                - count(self)
                - has_analyses(self)
                - first(self)
                - last(self)
                - add(self, analysis)
                - extend(self, other)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 sandhi_context.py
            🏗️ Classes:
              • class SandhiContext:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_source(self)
                - has_metadata(self)
                - metadata_count(self)
                - recursive(self)
                - multiple_splits_enabled(self)
                - get(self, key, default)
                - __str__(self)
        📄 sandhi_diagnostic.py
            🏗️ Classes:
              • class SandhiDiagnostic:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_info(self)
                - is_warning(self)
                - is_error(self)
                - has_rule(self)
                - has_location(self)
                - __str__(self)
        📄 sandhi_repository.py
            🏗️ Classes:
              • class SandhiRepository:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - get(self, identifier)
                - contains(self, identifier)
                - search(self, query)
                - all(self)
                - count(self)
        📄 sandhi_resolution_kernel.py
            🏗️ Classes:
              • class SandhiResolutionKernel:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - resolution_strategy(self)
                - build_context(self, context)
                - resolve(self, context)
                - __call__(self, context)
                - __str__(self)
        📄 sandhi_resolution_result.py
            🏗️ Classes:
              • class SandhiResolutionResult:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - result(self)
                - has_analyses(self)
                - analysis_count(self)
                - succeeded(self)
                - __str__(self)
        📄 sandhi_resolver.py
            🏗️ Classes:
              • class SandhiResolver:
                - __init__(self, strategy)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - strategy(self)
                - resolve(self, context)
                - __str__(self)
        📄 sandhi_result.py
            🏗️ Classes:
              • class SandhiResult:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - subject(self)
                - source(self)
                - language(self)
                - script(self)
                - has_diagnostics(self)
                - diagnostic_count(self)
                - has_errors(self)
                - has_warnings(self)
                - first_diagnostic(self)
                - resolved(self)
                - unresolved(self)
                - is_confident(self)
                - has_value(self)
                - candidate_count(self)
                - is_ambiguous(self)
                - __str__(self)
        📄 sandhi_rule.py
            🏗️ Classes:
              • class SandhiRule:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - applies_to(self, context)
                - apply(self, context)
                - __str__(self)
        📄 sandhi_rule_set.py
            🏗️ Classes:
              • class SandhiRuleSet:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_empty(self)
                - count(self)
                - apply(self, context)
                - add(self, rule)
                - __len__(self)
                - __iter__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 sandhi_service.py
            🏗️ Classes:
              • class SandhiService:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - resolution_kernel(self)
                - resolve(self, context)
                - contribute(self, aggregate)
                - __str__(self)
        📄 sandhi_strategy.py
            🏗️ Classes:
              • class SandhiStrategy:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - resolve(self, context)
                - __str__(self)
        📄 savarna_dirgha_rule.py
            🏗️ Classes:
              • class SavarnaDirghaRule:
                - display_name(self)
                - display_description(self)
                - _extract_words(self, context)
                - applies_to(self, context)
                - apply(self, context)
        📄 svara_sandhi_rule.py
            🏗️ Classes:
              • class SvaraSandhiRule:
                - display_name(self)
                - display_description(self)
        📄 upadhmaniya_rule.py
            🏗️ Classes:
              • class UpadhmaniyaRule:
                - display_name(self)
                - display_description(self)
                - _extract_words(self, context)
                - applies_to(self, context)
                - apply(self, context)
        📄 visarga_allophone_rule.py
            🏗️ Classes:
              • class VisargaAllophoneRule:
                - display_name(self)
                - display_description(self)
                - is_transformation_rule(self)
                - is_allophone_rule(self)
                - applies_to(self, context)
                - apply(self, context)
        📄 visarga_sandhi_rule.py
            🏗️ Classes:
              • class VisargaSandhiRule:
                - display_name(self)
                - display_description(self)
        📄 visarga_to_r_rule.py
            🏗️ Classes:
              • class VisargaToRRule:
                - display_name(self)
                - display_description(self)
                - _extract_words(self, context)
                - applies_to(self, context)
                - apply(self, context)
        📄 visarga_to_s_rule.py
            🏗️ Classes:
              • class VisargaToSRule:
                - display_name(self)
                - display_description(self)
                - _extract_words(self, context)
                - applies_to(self, context)
                - apply(self, context)
        📄 visarga_transformation_rule.py
            🏗️ Classes:
              • class VisargaTransformationRule:
                - display_name(self)
                - display_description(self)
                - is_transformation_rule(self)
                - is_allophone_rule(self)
                - applies_to(self, context)
                - apply(self, context)
        📄 vrddhi_sandhi_rule.py
            🏗️ Classes:
              • class VrddhiSandhiRule:
                - display_name(self)
                - display_description(self)
                - _extract_words(self, context)
                - applies_to(self, context)
                - apply(self, context)
        📄 vyanjana_sandhi_rule.py
            🏗️ Classes:
              • class VyanjanaSandhiRule:
                - display_name(self)
                - display_description(self)
      📂 semantic/
        📄 default_semantic_repository.py
            🏗️ Classes:
              • class DefaultSemanticRepository:
                - get(self, identifier)
                - search(self, query)
                - all(self)
                - count(self)
        📄 default_semantic_resolution_kernel.py
            🏗️ Classes:
              • class DefaultSemanticResolutionKernel:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - resolution_strategy(self)
                - kernel(self)
                - build_context(self, context)
                - resolve(self, context)
                - __call__(self, context)
                - __str__(self)
        📄 default_semantic_resolver.py
            🏗️ Classes:
              • class DefaultSemanticResolver:
                - __init__(self, strategy)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, context)
        📄 default_semantic_rule_set.py
            🔹 Constants:
              • DEFAULT_SEMANTIC_RULES
            ⚙️ Functions:
              • default_semantic_rule_set()
        📄 default_semantic_service.py
            🏗️ Classes:
              • class DefaultSemanticService:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - repository(self)
                - get_relation(self, identifier)
                - search_relations(self, query)
                - all_relations(self)
                - relation_count(self)
        📄 default_semantic_strategy.py
            🏗️ Classes:
              • class DefaultSemanticStrategy:
                - __init__(self, rule_set)
                - rule_set(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - _to_analysis_collection(self, context, candidates)
                - analyze(self, context)
        📄 semantic_analysis.py
            🏗️ Classes:
              • class SemanticAnalysis:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_meaning(self)
                - has_notes(self)
                - has_rule(self)
                - is_confident(self)
                - __str__(self)
        📄 semantic_analysis_collection.py
            🏗️ Classes:
              • class SemanticAnalysisCollection:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - count(self)
                - is_empty(self)
                - first(self)
                - add(self, analysis)
                - extend(self, other)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 semantic_analysis_result.py
            🏗️ Classes:
              • class SemanticAnalysisResult:
                - from_result(cls, result)
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - subject(self)
                - source(self)
                - language(self)
                - script(self)
                - has_analyses(self)
                - analysis_count(self)
                - first_analysis(self)
                - result(self)
                - has_diagnostics(self)
                - diagnostic_count(self)
                - first_diagnostic(self)
                - resolved(self)
                - unresolved(self)
                - is_confident(self)
                - to_result(self)
                - __str__(self)
        📄 semantic_concept.py
            🏗️ Classes:
              • class SemanticConcept:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_gloss(self)
                - has_category(self)
                - __str__(self)
        📄 semantic_concept_repository.py
            🔹 Constants:
              • DEFAULT_SEMANTIC_CONCEPTS
            🏗️ Classes:
              • class SemanticConceptRepository:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - get(self, identifier)
                - find_by_name(self, name)
                - search(self, query)
                - all(self)
                - contains(self, identifier)
                - count(self)
              • class DefaultSemanticConceptRepository:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - get(self, identifier)
                - find_by_name(self, name)
                - search(self, query)
                - all(self)
                - contains(self, identifier)
                - count(self)
        📄 semantic_context.py
            🏗️ Classes:
              • class SemanticContext:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_source(self)
                - has_metadata(self)
                - metadata_count(self)
                - recursive(self)
                - multiple_analyses_enabled(self)
                - get(self, key, default)
                - __str__(self)
        📄 semantic_diagnostic.py
            🏗️ Classes:
              • class SemanticDiagnostic:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_info(self)
                - is_warning(self)
                - is_error(self)
                - has_rule(self)
                - has_location(self)
                - __str__(self)
        📄 semantic_frame.py
            🏗️ Classes:
              • class SemanticFrame:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - concept_count(self)
                - relation_count(self)
                - has_concepts(self)
                - has_relations(self)
                - is_confident(self)
                - first_concept(self)
                - first_relation(self)
                - __iter__(self)
                - __len__(self)
                - __str__(self)
        📄 semantic_frame_builder.py
            🏗️ Classes:
              • class SemanticFrameBuilder:
                - _as_text(value)
                - _extract_text(value)
                - concept(identifier, name, gloss, category, description)
                - relation(identifier, relation, source, target, confidence, notes)
                - from_upstream(self, identifier, label, upstream)
                - from_vakya(self, identifier, vakya)
                - from_derivation(self, identifier, derivation)
                - from_samasa(self, identifier, samasa)
                - from_grammar(self, identifier, grammar)
        📄 semantic_graph.py
            🏗️ Classes:
              • class SemanticGraph:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - concept_count(self)
                - relation_count(self)
                - frame_count(self)
                - is_empty(self)
                - has_concepts(self)
                - has_relations(self)
                - has_frames(self)
                - first_concept(self)
                - first_relation(self)
                - first_frame(self)
                - get_concept(self, identifier)
                - get_relation(self, identifier)
                - get_frame(self, identifier)
                - find_concept_by_name(self, name)
                - concepts_by_category(self, category)
                - relations_by_type(self, relation_type)
                - add_concept(self, concept)
                - add_relation(self, relation)
                - add_frame(self, frame)
                - merge(self, other)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 semantic_graph_builder.py
            🏗️ Classes:
              • class SemanticGraphBuilder:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - _ensure_concept(self, graph, concept)
                - _ensure_relation(self, graph, relation)
                - _ensure_frame(self, graph, frame)
                - from_analysis(self, identifier, analyses)
                - from_upstream(self, identifier, upstream)
                - from_vakya(self, identifier, vakya)
                - from_derivation(self, identifier, derivation)
                - from_samasa(self, identifier, samasa)
                - from_grammar(self, identifier, grammar)
        📄 semantic_relation.py
            🏗️ Classes:
              • class SemanticRelation:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_notes(self)
                - is_confident(self)
                - __str__(self)
        📄 semantic_relation_collection.py
            🏗️ Classes:
              • class SemanticRelationCollection:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - count(self)
                - is_empty(self)
                - first(self)
                - add(self, relation)
                - extend(self, other)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 semantic_repository.py
            🏗️ Classes:
              • class SemanticRepository:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - get(self, identifier)
                - search(self, query)
                - all(self)
                - count(self)
        📄 semantic_resolution_kernel.py
            🏗️ Classes:
              • class SemanticResolutionKernel:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - resolution_strategy(self)
                - resolve(self, context)
                - _to_resolution_result(result)
                - __call__(self, context)
                - __str__(self)
        📄 semantic_resolution_result.py
            🏗️ Classes:
              • class SemanticResolutionResult:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - result(self)
                - has_analyses(self)
                - analysis_count(self)
                - succeeded(self)
                - __str__(self)
        📄 semantic_resolver.py
            🏗️ Classes:
              • class SemanticResolver:
                - __init__(self, strategy)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - strategy(self)
                - analyze(self, context)
                - __str__(self)
        📄 semantic_result.py
            🏗️ Classes:
              • class SemanticResult:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - subject(self)
                - source(self)
                - language(self)
                - script(self)
                - has_diagnostics(self)
                - diagnostic_count(self)
                - has_errors(self)
                - has_warnings(self)
                - first_diagnostic(self)
                - resolved(self)
                - unresolved(self)
                - is_confident(self)
                - has_value(self)
                - result(self)
                - __str__(self)
        📄 semantic_rule.py
            🏗️ Classes:
              • class SemanticRule:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - applies_to(self, context)
                - apply(self, context)
                - __str__(self)
        📄 semantic_rule_set.py
            🏗️ Classes:
              • class SemanticRuleSet:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_empty(self)
                - count(self)
                - add(self, rule)
                - apply(self, context)
                - __len__(self)
                - __iter__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 semantic_service.py
            🏗️ Classes:
              • class SemanticService:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - resolution_kernel(self)
                - resolve(self, context)
                - contribute(self, aggregate, context)
                - count(self)
                - __str__(self)
        📄 semantic_strategy.py
            🏗️ Classes:
              • class SemanticStrategy:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, context)
                - __str__(self)
        📄 semantic_upstream_rules.py
            🏗️ Classes:
              • class _UpstreamFrameRule:
                - __init__(self)
                - applies_to(self, context)
                - _frame(self, context, value)
                - apply(self, context)
              • class VakyaSemanticFrameRule:
                - display_name(self)
                - display_description(self)
              • class DerivationSemanticFrameRule:
                - display_name(self)
                - display_description(self)
              • class SamasaSemanticFrameRule:
                - display_name(self)
                - display_description(self)
              • class GrammarSemanticFrameRule:
                - display_name(self)
                - display_description(self)
      📂 vakya/
        📄 default_vakya_analyzer.py
            🏗️ Classes:
              • class DefaultVakyaAnalyzer:
                - __init__(self, rule_set)
                - rule_set(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - _to_analysis_collection(self, context, candidates)
                - analyze(self, context)
        📄 default_vakya_resolver.py
            🏗️ Classes:
              • class DefaultVakyaResolver:
                - __init__(self, strategy)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, context)
        📄 default_vakya_rule_set.py
            🔹 Constants:
              • DEFAULT_VAKYA_RULES
            ⚙️ Functions:
              • default_vakya_rule_set()
        📄 default_vakya_strategy.py
            🏗️ Classes:
              • class DefaultVakyaStrategy:
                - __init__(self, rule_set, parser)
                - rule_set(self)
                - parser(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - _parsed_structure(self, context)
                - _normalized_context(self, context)
                - _to_analysis_collection(self, context, candidates)
                - analyze(self, context)
        📄 upstream_vakya_rules.py
            🏗️ Classes:
              • class _MetadataUpstreamVakyaRule:
                - _describe(self, value)
                - _to_components(self, value)
                - applies_to(self, context)
                - apply(self, context)
              • class DerivationAwareVakyaRule:
                - display_name(self)
                - display_description(self)
              • class SamasaAwareVakyaRule:
                - display_name(self)
                - display_description(self)
              • class SandhiAwareVakyaRule:
                - display_name(self)
                - display_description(self)
              • class GrammarAwareVakyaRule:
                - display_name(self)
                - display_description(self)
        📄 vakya_analysis.py
            🏗️ Classes:
              • class VakyaAnalysis:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_rule(self)
                - has_notes(self)
                - is_confident(self)
                - __str__(self)
        📄 vakya_analysis_collection.py
            🏗️ Classes:
              • class VakyaAnalysisCollection:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - count(self)
                - is_empty(self)
                - first(self)
                - add(self, analysis)
                - extend(self, other)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 vakya_context.py
            🏗️ Classes:
              • class VakyaContext:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_source(self)
                - has_metadata(self)
                - metadata_count(self)
                - recursive(self)
                - multiple_analyses_enabled(self)
                - get(self, key, default)
                - __str__(self)
        📄 vakya_diagnostic.py
            🏗️ Classes:
              • class VakyaDiagnostic:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_info(self)
                - is_warning(self)
                - is_error(self)
                - has_rule(self)
                - has_location(self)
                - __str__(self)
        📄 vakya_parser.py
            🏗️ Classes:
              • class VakyaRole:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_value(self)
                - is_confident(self)
                - __str__(self)
              • class VakyaParseResult:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - role_count(self)
                - has_roles(self)
                - first_role(self)
                - get(self, key, default)
                - __iter__(self)
                - __len__(self)
                - __getitem__(self, index)
                - __str__(self)
              • class VakyaParser:
                - _as_tuple(value)
                - _extract_hint_roles(self, metadata)
                - _extract_upstream_roles(self, metadata)
                - _extract_token_roles(self, structure)
                - parse(self, identifier, sentence)
        📄 vakya_resolver.py
            🏗️ Classes:
              • class VakyaResolver:
                - __init__(self, strategy)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - strategy(self)
                - analyze(self, context)
                - __str__(self)
        📄 vakya_result.py
            🏗️ Classes:
              • class VakyaResult:
                - identifier(self)
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - subject(self)
                - source(self)
                - language(self)
                - script(self)
                - has_analyses(self)
                - analysis_count(self)
                - first_analysis(self)
                - result(self)
                - has_diagnostics(self)
                - diagnostic_count(self)
                - has_errors(self)
                - has_warnings(self)
                - first_diagnostic(self)
                - resolved(self)
                - unresolved(self)
                - is_confident(self)
                - best_analysis(self)
                - __str__(self)
        📄 vakya_rule.py
            🏗️ Classes:
              • class VakyaRule:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - applies_to(self, context)
                - apply(self, context)
                - __str__(self)
              • class UpstreamCompositionRule:
                - display_name(self)
                - display_description(self)
                - applies_to(self, context)
                - apply(self, context)
              • class StringSentenceRule:
                - display_name(self)
                - display_description(self)
                - applies_to(self, context)
                - apply(self, context)
        📄 vakya_rule_set.py
            🏗️ Classes:
              • class VakyaRuleSet:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - is_empty(self)
                - count(self)
                - add(self, rule)
                - apply(self, context)
                - __len__(self)
                - __iter__(self)
                - __getitem__(self, index)
                - __str__(self)
        📄 vakya_strategy.py
            🏗️ Classes:
              • class VakyaStrategy:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - analyze(self, context)
                - __str__(self)
        📄 vakya_structure.py
            🔹 Constants:
              • _SENTENCE_PUNCTUATION_RE
            🏗️ Classes:
              • class VakyaStructure:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - component_count(self)
                - has_components(self)
                - has_metadata(self)
                - get(self, key, default)
                - __str__(self)
                - normalize(cls, identifier, sentence)
                - from_sentence(cls, identifier, sentence)
    📂 exporters/
      📄 __init__.py
      📄 csv_export.py
          ⚙️ Functions:
            • export_words_csv(words)
      📄 html_export.py
          ⚙️ Functions:
            • export_html(title, body)
      📄 json_export.py
          ⚙️ Functions:
            • export_json(data)
      📄 pdf_export.py
          ⚙️ Functions:
            • export_pdf(*_args, **_kwargs)
    📂 input/
      📄 __init__.py
      📄 converter.py
          ⚙️ Functions:
            • to_devanagari(text)
      📄 detector.py
          ⚙️ Functions:
            • detect_script(text)
      📄 normalizer.py
          🔹 Constants:
            • DEVANAGARI_DIGITS
          ⚙️ Functions:
            • normalize_text(text)
      📄 reader.py
          ⚙️ Functions:
            • read_text(path)
    📂 interfaces/
      📄 __init__.py
      📄 analyzer.py
          🏗️ Classes:
            • class AnalyzerInterface:
              - analyze(self, tokens)
      📄 dictionary.py
          🏗️ Classes:
            • class DictionaryInterface:
              - lookup(self, word)
      📄 exporter.py
          🏗️ Classes:
            • class ExporterInterface:
              - export_json(self, name, result)
      📄 translator.py
          🏗️ Classes:
            • class TranslatorInterface:
              - translate(self, result)
    📂 lexical/
      📄 __init__.py
      📂 builders/
        📄 base_lexical_builder.py
            🏗️ Classes:
              • class BaseLexicalBuilder:
        📄 base_lexical_record_builder.py
            🏗️ Classes:
              • class BaseLexicalRecordBuilder:
                - record_type(self)
                - normalize_text(self, text)
                - normalize_optional(self, text)
        📄 lexeme_builder.py
            🏗️ Classes:
              • class LexemeBuilder:
                - __init__(self)
                - with_identifier(self, identifier)
                - with_lemma(self, lemma)
                - with_transliteration(self, transliteration)
                - with_part_of_speech(self, part_of_speech)
                - with_root(self, root)
                - with_frequency(self, frequency)
                - with_language(self, language)
                - with_script(self, script)
                - build(self)
        📄 lexeme_record_builder.py
            🏗️ Classes:
              • class LexemeRecordBuilder:
                - __init__(self)
                - record_type(self)
                - build(self, record)
        📄 lexical_relation_builder.py
            🏗️ Classes:
              • class LexicalRelationBuilder:
                - __init__(self)
                - with_identifier(self, identifier)
                - with_relation_type(self, relation_type)
                - between(self, source_identifier, target_identifier)
                - directed(self, directed)
                - with_weight(self, weight)
                - with_confidence(self, confidence)
                - build(self)
      📂 enums/
        📄 lexical_status.py
            🏗️ Classes:
              • class LexicalStatus:
        📄 part_of_speech.py
            🏗️ Classes:
              • class PartOfSpeech:
        📄 relation_type.py
            🏗️ Classes:
              • class RelationType:
      📂 models/
        📄 base_lexical_metadata.py
            🏗️ Classes:
              • class BaseLexicalMetadata:
                - has_lemma(self)
                - has_transliteration(self)
                - has_root(self)
                - has_aliases(self)
                - alias_count(self)
                - is_published(self)
                - is_verified(self)
        📄 base_lexical_node.py
            🏗️ Classes:
              • class BaseLexicalNode:
                - __init__(self, identifier, metadata)
                - label(self)
        📄 dictionary_entry.py
            🏗️ Classes:
              • class DictionaryEntry:
                - __init__(self, identifier, metadata, source)
                - dictionary_name(self)
                - dictionary_version(self)
                - entry_identifier(self)
                - headword(self)
                - transliteration(self)
                - volume(self)
                - chapter(self)
                - section(self)
                - page(self)
                - entry_number(self)
                - editor(self)
                - publisher(self)
                - publication_year(self)
                - is_primary(self)
                - citation(self)
                - display_title(self)
        📄 dictionary_entry_metadata.py
            🏗️ Classes:
              • class DictionaryEntryMetadata:
                - display_title(self)
                - has_dictionary(self)
                - has_headword(self)
                - has_location(self)
                - citation(self)
        📄 dictionary_sense.py
            🏗️ Classes:
              • class DictionarySense:
                - __init__(self, identifier, metadata)
                - sense_number(self)
                - definition(self)
                - short_definition(self)
                - gloss(self)
                - semantic_domain(self)
                - usage_label(self)
                - register(self)
                - grammatical_note(self)
                - etymology(self)
                - examples(self)
                - citations(self)
                - cross_references(self)
        📄 dictionary_sense_metadata.py
            🏗️ Classes:
              • class DictionarySenseMetadata:
        📄 lexeme.py
            🏗️ Classes:
              • class Lexeme:
                - __init__(self, identifier, metadata)
                - lemma(self)
                - transliteration(self)
                - part_of_speech(self)
                - root(self)
                - frequency(self)
                - language(self)
                - script(self)
                - status(self)
        📄 lexeme_metadata.py
            🏗️ Classes:
              • class LexemeMetadata:
                - display_title(self)
                - has_title(self)
                - canonical_name(self)
                - is_known(self)
                - from_lemma(cls, lemma)
        📄 lexical_record.py
            🏗️ Classes:
              • class LexicalRecord:
                - __init__(self, identifier, metadata, source)
                - source(self)
                - source_name(self)
                - source_identifier(self)
        📄 lexical_relation.py
            🏗️ Classes:
              • class LexicalRelation:
                - __init__(self, identifier, metadata)
                - relation_type(self)
                - source_identifier(self)
                - target_identifier(self)
                - directed(self)
                - weight(self)
                - confidence(self)
                - source_dictionary(self)
        📄 lexical_relation_metadata.py
            🏗️ Classes:
              • class LexicalRelationMetadata:
        📄 lexical_source.py
            🏗️ Classes:
              • class LexicalSource:
                - display_name(self)
                - display_text(self)
                - display_description(self)
                - has_version(self)
                - has_publisher(self)
                - has_editor(self)
                - has_website(self)
                - __str__(self)
        📄 lexical_source_metadata.py
            🏗️ Classes:
              • class LexicalSourceMetadata:
      📂 monier_williams/
        📄 __init__.py
        📄 parser.py
            🔹 Constants:
              • _FIELD_PATTERN
            🏗️ Classes:
              • class MonierWilliamsParser:
                - parse(self, lines)
                - _build_record(self, lines)
        📄 record.py
            🏗️ Classes:
              • class MonierWilliamsRecord:
                - add_line(self, line)
                - text(self)
      📂 parsers/
        📄 base_lexical_parser.py
            🏗️ Classes:
              • class BaseLexicalParser:
                - normalize_text(self, text)
                - normalize_optional(self, text)
                - parse_lines(self, lines)
                - subsystem(self)
      📂 records/
        📄 lexeme_record.py
            🏗️ Classes:
              • class LexemeRecord:
                - display_text(self)
      📂 registries/
        📄 __init__.py
        📄 lexical_registry.py
            🏗️ Classes:
              • class LexicalRegistry:
                - register_many(self, objects)
                - lexemes(self)
                - dictionary_entries(self)
                - dictionary_senses(self)
                - lexical_relations(self)
        📄 lexical_source_catalog.py
            🏗️ Classes:
              • class LexicalSourceCatalog:
                - __init__(self, sources)
                - register(self, source)
                - register_many(self, sources)
                - get(self, identifier)
                - require(self, identifier)
                - exists(self, identifier)
                - remove(self, identifier)
                - clear(self)
                - identifiers(self)
                - sources(self)
                - count(self)
                - __contains__(self, identifier)
                - __len__(self)
                - __iter__(self)
                - _normalize_identifier(identifier)
      📂 repositories/
        📄 in_memory_lexical_repository.py
            🏗️ Classes:
              • class InMemoryLexicalRepository:
                - __init__(self, source)
                - source(self)
                - add(self, lexical_object)
                - add_many(self, lexical_objects)
                - get_lexeme(self, identifier)
                - get_entry(self, identifier)
                - get_sense(self, identifier)
                - find_by_lemma(self, lemma)
                - find_by_transliteration(self, transliteration)
                - contains(self, identifier)
                - search(self, query)
                - _matches_lexeme(lexeme, query)
                - _matches_entry(entry, query)
                - _matches_sense(sense, query)
                - lexeme_count(self)
                - entry_count(self)
                - sense_count(self)
                - count(self)
                - clear(self)
        📄 lexical_repository.py
            🏗️ Classes:
              • class LexicalRepository:
                - source(self)
                - get_lexeme(self, identifier)
                - get_entry(self, identifier)
                - get_sense(self, identifier)
                - find_by_lemma(self, lemma)
                - find_by_transliteration(self, transliteration)
                - contains(self, identifier)
                - search(self, query)
      📂 validators/
        📄 base_lexical_validator.py
            🏗️ Classes:
              • class BaseLexicalValidator:
        📄 dictionary_entry_validator.py
            🏗️ Classes:
              • class DictionaryEntryValidator:
                - validate(self, obj)
        📄 dictionary_sense_validator.py
            🏗️ Classes:
              • class DictionarySenseValidator:
                - validate(self, obj)
        📄 lexeme_validator.py
            🏗️ Classes:
              • class LexemeValidator:
                - validate(self, obj)
        📄 lexical_relation_validator.py
            🏗️ Classes:
              • class LexicalRelationValidator:
                - validate(self, obj)
        📄 lexical_source_validator.py
            🏗️ Classes:
              • class LexicalSourceValidator:
                - validate(self, obj)
    📂 models/
      📄 __init__.py
      📄 analysis_result.py
          🏗️ Classes:
            • class AnalysisResult:
              - to_dict(self)
      📄 base.py
          🏗️ Classes:
            • class BaseModel:
              - touch(self)
              - set_status(self, status)
              - add_metadata(self, key, value)
              - to_dict(self)
              - from_dict(cls, data)
              - summary(self)
              - __repr__(self)
      📄 meaning.py
          🏗️ Classes:
            • class Meaning:
              - summary(self)
      📄 pipeline_state.py
          🏗️ Classes:
            • class PipelineState:
              - start(self)
              - finish(self)
              - advance(self, stage)
              - add_warning(self, message)
              - add_error(self, message)
              - is_complete(self)
              - summary(self)
      📄 samasa_analysis.py
          🏗️ Classes:
            • class SamasaAnalysis:
              - add_member(self, word)
              - add_alternative(self, analysis)
              - compound_text(self)
              - summary(self)
      📄 sandhi_analysis.py
          🏗️ Classes:
            • class SandhiAnalysis:
              - add_alternative(self, analysis)
              - left_text(self)
              - right_text(self)
              - result_text(self)
              - summary(self)
      📄 sentence.py
          🏗️ Classes:
            • class Sentence:
              - start_analysis(self)
              - finish_analysis(self)
              - set_stage(self, stage)
              - add_original_word(self, word)
              - add_word(self, word)
              - word_count(self)
              - text(self)
              - normalize(self)
              - tokenize(self)
              - padaccheda_complete(self)
              - morphology_complete(self)
              - grammar_complete(self)
              - translation_complete(self)
              - summary(self)
              - __str__(self)
      📄 sloka.py
          🏗️ Classes:
            • class Sloka:
      📄 word.py
          🏗️ Classes:
            • class Word:
              - __post_init__(self)
              - normalize(self, text)
              - add_meaning(self, meaning)
              - add_lexeme(self, lexeme_id)
              - add_concept(self, concept_id)
              - set_feature(self, name, value)
              - get_feature(self, name, default)
              - summary(self)
      📂 amarakosha/
        📄 __init__.py
        📄 amarakosha.py
            🏗️ Classes:
              • class Amarakosha:
                - __post_init__(self)
                - add_kanda(self, kanda)
                - get_kanda(self, kanda_id)
                - remove_kanda(self, kanda_id)
                - clear(self)
                - kanda_count(self)
                - varga_count(self)
                - verse_count(self)
                - first_kanda(self)
                - last_kanda(self)
                - kanda_ids(self)
                - find_varga(self, varga_id)
                - find_verse(self, verse_id)
                - to_dict(self)
                - __len__(self)
                - __iter__(self)
                - __contains__(self, kanda_id)
                - __str__(self)
                - __repr__(self)
        📄 kanda.py
            🏗️ Classes:
              • class Kanda:
                - __post_init__(self)
                - add_varga(self, varga)
                - get_varga(self, varga_id)
                - remove_varga(self, varga_id)
                - clear(self)
                - varga_count(self)
                - verse_count(self)
                - first_varga(self)
                - last_varga(self)
                - varga_ids(self)
                - to_dict(self)
                - __len__(self)
                - __iter__(self)
                - __contains__(self, varga_id)
                - __str__(self)
                - __repr__(self)
        📄 varga.py
            🏗️ Classes:
              • class Varga:
                - __post_init__(self)
                - add_verse(self, verse)
                - get_verse(self, verse_id)
                - remove_verse(self, verse_id)
                - clear(self)
                - verse_count(self)
                - first_verse(self)
                - last_verse(self)
                - verse_ids(self)
                - to_dict(self)
                - __len__(self)
                - __iter__(self)
                - __contains__(self, verse_id)
                - __str__(self)
                - __repr__(self)
        📄 verse.py
            🏗️ Classes:
              • class Verse:
                - __post_init__(self)
                - add_token(self, token)
                - clear_tokens(self)
                - token_count(self)
                - add_lexeme(self, lexeme_id)
                - clear_lexemes(self)
                - lexeme_count(self)
                - to_dict(self)
                - __str__(self)
                - __repr__(self)
      📂 enums/
        📄 case.py
            🏗️ Classes:
              • class Case:
        📄 dictionary_source.py
            🏗️ Classes:
              • class DictionarySource:
        📄 gender.py
            🏗️ Classes:
              • class Gender:
        📄 lakara.py
            🏗️ Classes:
              • class Lakara:
        📄 language.py
            🏗️ Classes:
              • class Language:
        📄 number.py
            🏗️ Classes:
              • class Number:
        📄 part_of_speech.py
            🏗️ Classes:
              • class PartOfSpeech:
        📄 person.py
            🏗️ Classes:
              • class Person:
        📄 pipeline_stage.py
            🏗️ Classes:
              • class PipelineStage:
        📄 relation_type.py
            🏗️ Classes:
              • class RelationType:
                - values(cls)
                - names(cls)
                - has_value(cls, value)
        📄 samasa.py
            🏗️ Classes:
              • class Samasa:
        📄 sandhi.py
            🏗️ Classes:
              • class Sandhi:
        📄 script.py
            🏗️ Classes:
              • class Script:
        📄 status.py
            🏗️ Classes:
              • class Status:
        📄 tense.py
            🏗️ Classes:
              • class Tense:
        📄 voice.py
            🏗️ Classes:
              • class Voice:
      📂 imports/
        📄 __init__.py
        📄 import_configuration.py
            🏗️ Classes:
              • class ImportConfiguration:
                - validation_enabled(self)
                - lexical_processing_enabled(self)
                - to_dict(self)
                - __repr__(self)
        📄 import_error.py
            🏗️ Classes:
              • class ImportError:
                - __post_init__(self)
                - is_info(self)
                - is_warning(self)
                - is_error(self)
                - is_fatal(self)
                - location(self)
                - to_dict(self)
                - __str__(self)
                - __repr__(self)
        📄 import_result.py
            🏗️ Classes:
              • class ImportResult:
                - __post_init__(self)
                - add_document(self, identifier)
                - add_unit(self, identifier)
                - skip_unit(self, identifier)
                - add_error(self, error)
                - warning(self, message)
                - error(self, message)
                - add_metadata(self, key, value)
                - set_metadata(self, key, value)
                - increment(self, key, amount)
                - warning_count(self)
                - error_count(self)
                - has_errors(self)
                - has_warnings(self)
                - successful(self)
                - duration_seconds(self)
                - document_count(self)
                - unit_count(self)
                - finalize(self)
                - finish(self)
                - merge(self, other)
                - to_dict(self)
                - __bool__(self)
                - __len__(self)
                - __str__(self)
                - __repr__(self)
        📄 import_statistics.py
            🏗️ Classes:
              • class ImportStatistics:
                - start(self)
                - stop(self)
                - elapsed_seconds(self)
                - imported_objects(self)
                - lexical_objects(self)
                - has_errors(self)
                - has_warnings(self)
                - reset(self)
                - to_dict(self)
                - __str__(self)
                - __repr__(self)
        📄 import_status.py
            🏗️ Classes:
              • class ImportStatus:
                - is_finished(self)
                - is_success(self)
                - is_failure(self)
                - has_warnings(self)
                - __str__(self)
                - __repr__(self)
      📂 lexical/
        📄 __init__.py
        📄 dictionary_entry.py
            🏗️ Classes:
              • class DictionaryEntry:
                - __post_init__(self)
                - identity(self)
                - source_key(self)
                - sense_count(self)
                - add_sense(self, sense)
                - get_sense(self, sense_id)
                - has_sense(self, sense_id)
                - to_dict(self)
                - __str__(self)
                - __repr__(self)
        📄 dictionary_sense.py
            🏗️ Classes:
              • class DictionarySense:
                - __post_init__(self)
                - add_example(self, example)
                - example_count(self)
                - to_dict(self)
                - __str__(self)
                - __repr__(self)
        📄 lexeme.py
            🏗️ Classes:
              • class Lexeme:
                - __post_init__(self)
                - add_dictionary_entry(self, entry)
                - get_entry(self, source)
                - has_entry(self, source)
                - remove_entry(self, source)
                - add_relation(self, relation)
                - dictionary_count(self)
                - relation_count(self)
                - dictionary_sources(self)
                - to_dict(self)
                - __str__(self)
                - __repr__(self)
        📄 lexical_relation.py
            🏗️ Classes:
              • class LexicalRelation:
                - __post_init__(self)
                - identity(self)
                - to_dict(self)
                - __str__(self)
                - __repr__(self)
    📂 pipeline/
      📄 __init__.py
      📄 pipeline.py
          🏗️ Classes:
            • class AnalysisPipeline:
              - __init__(self, dictionary, normalizer, tokenizer, grammar)
              - run(self, text)
      📄 stages.py
          🏗️ Classes:
            • class PipelineContext:
            • class PipelineStage:
              - run(self, context)
    📂 plugins/
      📄 __init__.py
      📂 amarakosha/
        📄 __init__.py
        📄 plugin.py
            🏗️ Classes:
              • class Plugin:
                - lookup(self, word)
      📂 dhatupatha/
        📄 __init__.py
        📄 plugin.py
            🏗️ Classes:
              • class Plugin:
                - lookup(self, word)
      📂 heritage/
        📄 __init__.py
        📄 plugin.py
            🏗️ Classes:
              • class Plugin:
                - lookup(self, word)
      📂 puranas/
        📄 __init__.py
        📄 plugin.py
            🏗️ Classes:
              • class Plugin:
                - lookup(self, word)
      📂 sanskritnlp/
        📄 __init__.py
        📄 plugin.py
            🏗️ Classes:
              • class Plugin:
                - lookup(self, word)
      📂 vedas/
        📄 __init__.py
        📄 plugin.py
            🏗️ Classes:
              • class Plugin:
                - lookup(self, word)
    📂 registry/
      📄 __init__.py
      📄 analyzer_registry.py
          🏗️ Classes:
            • class AnalyzerRegistry:
              - __init__(self)
              - register(self, name, analyzer)
              - get(self, name)
              - names(self)
      📄 plugin_registry.py
          🏗️ Classes:
            • class PluginRegistry:
              - __init__(self)
              - register_dictionary(self, plugin)
              - get_dictionary(self, name)
              - dictionaries(self)
    📂 scripts/
      📄 audit_amarakosha_imports.py
          🔹 Constants:
            • ROOT
            • TARGETS
      📄 backup_database.py
          ⚙️ Functions:
            • main()
      📄 build_dictionary.py
          ⚙️ Functions:
            • build_dictionary(csv_path, output_path)
            • main()
      📄 import_amarakosha.py
          ⚙️ Functions:
            • main()
      📄 import_puranas.py
          ⚙️ Functions:
            • main()
      📄 prototype_reader_utility.py
          🔹 Constants:
            • SLOKA_IAST
          ⚙️ Functions:
            • tokenize_iast(text)
            • guess_root_iast(word_iast)
            • iast_to_devanagari(text_iast)
            • fetch_wiktionary_extract(word_deva)
            • extract_sanskrit_section(extract)
            • analyze_sloka_with_readable_definitions(sloka_iast)
          🏗️ Classes:
            • class LexicalPreviewResult:
      📄 rebuild_indexes.py
          ⚙️ Functions:
            • main()
    📂 services/
      📄 __init__.py
      📄 analysis_service.py
          🏗️ Classes:
            • class AnalysisService:
              - __init__(self, dictionary, normalizer, tokenizer, grammar)
              - analyze(self, text)
      📄 dictionary_service.py
          🏗️ Classes:
            • class DictionaryService:
              - __init__(self, dictionary, registry)
              - lookup(self, word, plugin_name)
      📄 export_service.py
          🏗️ Classes:
            • class ExportService:
              - __init__(self, storage)
              - export_json(self, name, result)
      📄 grammar_service.py
          🏗️ Classes:
            • class GrammarService:
              - __init__(self, dictionary)
              - analyze_tokens(self, tokens)
      📄 lexical_repository.py
      📄 lexical_repository_backup.py
          🏗️ Classes:
            • class LexicalRepository:
              - __init__(self)
              - add(self, lexeme)
              - remove(self, lexeme_id)
              - get(self, lexeme_id)
              - by_lemma(self, lemma)
              - by_transliteration(self, transliteration)
              - by_dictionary(self, source, headword)
              - contains(self, lexeme_id)
              - all(self)
              - clear(self)
              - lexeme_count(self)
              - dictionary_sources(self)
              - add_dictionary_entry(self, lexeme_id, entry)
              - to_dict(self)
              - __len__(self)
              - __iter__(self)
              - __repr__(self)
      📄 normalization_service.py
          🏗️ Classes:
            • class NormalizationService:
              - normalize(self, text)
      📄 tokenizer_service.py
          🏗️ Classes:
            • class TokenizerService:
              - tokenize(self, text)
      📄 translation_service.py
          🏗️ Classes:
            • class TranslationService:
              - translate(self, result)
      📂 importers/
        📄 __init__.py
        📄 amarakosha_builder.py
            🏗️ Classes:
              • class AmarakoshaBuilder:
                - build_kanda(number, title)
                - build_varga(number, title)
                - build_verse(number, text)
        📄 amarakosha_importer.py
            🏗️ Classes:
              • class AmarakoshaImporter:
                - __init__(self, configuration)
                - import_file(self, file_path)
                - import_text(self, text)
                - parser_name(self)
                - __repr__(self)
        📄 amarakosha_parser.py
            🔹 Constants:
              • DEFAULT_ENCODING
              • SUPPORTED_EXTENSIONS
            🏗️ Classes:
              • class AmarakoshaParser:
                - __init__(self, configuration)
                - context(self)
                - _increment_stat(self, stat_name, delta)
                - parse_file(self, path)
                - parse_text(self, text)
                - parse_lines(self, lines)
                - _safe_error_transition(self)
                - _engine_loop(self, lines)
                - _dispatch_safely(self, result)
                - _handle_kanda(self, result)
                - _handle_varga(self, result)
                - _handle_verse(self, result)
                - _handle_empty(self, result)
                - _handle_comment(self, result)
                - _handle_unknown(self, result)
                - _finalize_pipeline(self)
                - __repr__(self)
        📄 classification_result.py
            🏗️ Classes:
              • class ClassificationResult:
        📄 import_result_builder.py
            🏗️ Classes:
              • class ImportResultBuilder:
                - __init__(self)
                - with_status(self, status)
                - with_importer_name(self, importer_name)
                - with_source_file(self, source_file)
                - with_message(self, message)
                - with_imported_object(self, imported_object)
                - with_book(self, book)
                - with_imported_documents(self, documents)
                - with_imported_units(self, units)
                - with_skipped_units(self, units)
                - with_statistics(self, statistics)
                - with_errors(self, errors)
                - with_metadata(self, metadata)
                - build(self)
        📄 line_classifier.py
            🏗️ Classes:
              • class LineType:
                - __str__(self)
              • class LineClassifier:
                - classify(cls, line)
                - is_structural(cls, line)
                - is_ignorable(cls, line)
                - __repr__(self)
        📄 parser_context.py
            🏗️ Classes:
              • class ParserContext:
                - __init__(self, edition_id)
                - current_kanda(self)
                - current_varga(self)
                - current_verse(self)
                - next_line(self, line)
                - transition(self, next_state)
                - enter_kanda(self, kanda)
                - enter_varga(self, varga)
                - enter_verse(self, verse)
                - add_error(self, message, severity)
        📄 parser_errors.py
            🏗️ Classes:
              • class ParserError:
                - __init__(self, message, line_number)
              • class RecoverableParserError:
              • class FatalParserError:
              • class StructureError:
              • class ValidationError:
        📄 parser_state.py
            🏗️ Classes:
              • class ParserState:
                - is_terminal(self)
                - expects_structure(self)
                - is_running(self)
                - can_transition_to(self, next_state)
                - __str__(self)
                - __repr__(self)
        📄 parser_validator.py
            🏗️ Classes:
              • class ParserValidator:
                - validate_transition(current_state, next_state, line_number)
                - validate_hierarchy_presence(active_parent, entity_type, line_number)
                - validate_completion(book)
        📄 structure_numbering.py
            🏗️ Classes:
              • class StructureNumbering:
                - next_kanda_number(book)
                - next_varga_number(active_kanda)
                - next_verse_number(active_varga)
        📄 unicode_normalizer.py
            🏗️ Classes:
              • class UnicodeNormalizer:
                - normalize(cls, text)
                - normalize_unicode(text)
                - remove_bom(cls, text)
                - remove_zero_width(cls, text)
                - normalize_line_endings(text)
                - normalize_tabs(text)
                - normalize_spaces(text)
                - strip_trailing_whitespace(text)
                - normalize_lines(cls, text)
                - is_normalized(text)
                - __repr__(self)
      📂 repositories/
        📄 __init__.py
        📄 lexical_repository_base.py
            🏗️ Classes:
              • class LexicalRepositoryBase:
                - add(self, lexeme)
                - update(self, lexeme)
                - remove(self, lexeme_id)
                - clear(self)
                - get(self, lexeme_id)
                - by_lemma(self, lemma)
                - by_transliteration(self, transliteration)
                - find_by_dictionary(self, source, headword)
                - add_dictionary_entry(self, lexeme_id, entry)
                - exists(self, lexeme_id)
                - all(self)
                - __iter__(self)
                - __len__(self)
                - lexeme_count(self)
        📄 lexical_repository_factory.py
            🏗️ Classes:
              • class LexicalRepositoryFactory:
                - register(cls, backend, repository_class)
                - create(cls, backend)
                - available_backends(cls)
                - is_supported(cls, backend)
                - __repr__(self)
        📄 memory_lexical_repository.py
            🏗️ Classes:
              • class MemoryLexicalRepository:
                - __init__(self)
                - _index_lexeme(self, lexeme)
                - _deindex_lexeme(self, lexeme)
                - add(self, lexeme)
                - update(self, lexeme)
                - remove(self, lexeme_id)
                - get(self, lexeme_id)
                - by_lemma(self, lemma)
                - by_transliteration(self, transliteration)
                - find_by_dictionary(self, source, headword)
                - add_dictionary_entry(self, lexeme_id, entry)
                - exists(self, lexeme_id)
                - all(self)
                - clear(self)
                - dictionary_sources(self)
                - to_dict(self)
                - __iter__(self)
                - __len__(self)
                - __contains__(self, lexeme_id)
                - __repr__(self)
    📂 storage/
      📄 __init__.py
      📄 connection.py
          🏗️ Classes:
            • class DatabaseConnection:
              - __init__(self, dsn)
              - connect(self)
      📄 json_storage.py
          🏗️ Classes:
            • class JsonStorage:
              - __init__(self, output_dir)
              - save(self, name, data)
      📄 postgres_storage.py
          🏗️ Classes:
            • class PostgresStorage:
              - __init__(self, dsn)
              - connect(self)
      📂 migrations/
        📄 __init__.py
      📂 repositories/
        📄 __init__.py
        📄 corpus_repository.py
            🏗️ Classes:
              • class CorpusRepository:
                - __init__(self)
                - add(self, record)
                - search(self, query)
        📄 sloka_repository.py
            🏗️ Classes:
              • class SlokaRepository:
                - __init__(self)
                - add(self, sloka)
                - all(self)
        📄 word_repository.py
            🏗️ Classes:
              • class WordRepository:
                - __init__(self)
                - save(self, word)
                - get(self, text)
    📂 tests/
      📄 __init__.py
      📄 test_derivation_pratyaya_vakya_flow.py
          🏗️ Classes:
            • class TestKernelFlow:
              - test_end_to_end_flow(self)
              - test_dhatu_lookup_still_works(self)
      📄 test_dictionary.py
          ⚙️ Functions:
            • test_dictionary_lookup_sample_entry()
      📄 test_normalizer.py
          ⚙️ Functions:
            • test_normalizer_spaces_danda()
      📄 test_padaccheda.py
          ⚙️ Functions:
            • test_padaccheda_placeholder_returns_input()
      📄 test_pipeline.py
          ⚙️ Functions:
            • test_pipeline_finds_dictionary_meaning()
      📄 test_services.py
          ⚙️ Functions:
            • test_analysis_service_uses_injected_dictionary()
            • test_translation_service_uses_known_meanings()
      📄 test_sloka.py
          ⚙️ Functions:
            • test_sloka_holds_text()
      📄 test_tokenizer.py
          ⚙️ Functions:
            • test_tokenizer_handles_devanagari_and_danda()
      📄 test_word.py
          ⚙️ Functions:
            • test_word_defaults_to_empty_features()
      📂 acquisition/
        📄 _updated_make_manifest.py
            ⚙️ Functions:
              • make_manifest()
        📄 test_acquisition_manifest.py
            ⚙️ Functions:
              • make_source()
              • make_manifest()
              • test_manifest_construction()
              • test_url_management()
              • test_duplicate_urls_are_ignored()
              • test_empty_urls_are_ignored()
              • test_download_requirement()
              • test_checksum_requirement()
              • test_license_validation_requirement()
              • test_metadata()
              • test_to_dict()
              • test_repr_contains_identity()
        📄 test_acquisition_pipeline.py
            ⚙️ Functions:
              • make_source()
              • make_manifest()
              • test_pipeline_delegates_to_acquirer()
              • test_pipeline_run_is_alias_for_acquire()
              • test_pipeline_display()
              • test_pipeline_is_frozen()
            🏗️ Classes:
              • class FakeSourceAcquirer:
                - __init__(self)
                - acquire(self, manifest)
        📄 test_acquisition_result.py
            ⚙️ Functions:
              • make_source()
              • test_result_construction()
              • test_finalize_sets_completion_information()
              • test_warning_management()
              • test_empty_warning_is_ignored()
              • test_error_marks_result_failed()
              • test_empty_error_is_ignored()
              • test_downloaded_files()
              • test_extracted_files()
              • test_metadata()
              • test_to_dict()
              • test_repr_contains_identity()
        📄 test_acquisition_service.py
            ⚙️ Functions:
              • test_acquisition_service_is_abstract()
              • test_acquisition_service_cannot_be_instantiated()
        📄 test_corpus_source.py
            ⚙️ Functions:
              • make_source()
              • test_corpus_source_construction()
              • test_default_state()
              • test_download_url_management()
              • test_duplicate_download_urls_are_ignored()
              • test_tag_management()
              • test_empty_tag_is_ignored()
              • test_metadata_management()
              • test_local_path_and_filename()
              • test_status_and_importability()
              • test_to_dict()
              • test_repr_contains_identity()
        📄 test_default_acquisition_service.py
            ⚙️ Functions:
              • make_source()
              • make_manifest()
              • make_service()
              • test_default_service_delegates_to_pipeline()
              • test_default_service_run_alias()
              • test_default_service_display()
              • test_default_service_is_frozen()
            🏗️ Classes:
              • class FakeSourceAcquirer:
                - __init__(self)
                - acquire(self, manifest)
        📄 test_default_source_acquirer.py
            ⚙️ Functions:
              • make_source(identifier)
              • file_url(path)
              • make_manifest()
              • test_successful_local_file_acquisition(tmp_path)
              • test_result_is_finalized(tmp_path)
              • test_existing_destination_file_is_rejected_by_default(tmp_path)
              • test_existing_destination_can_be_overwritten(tmp_path)
              • test_failed_primary_url_falls_back_to_mirror(tmp_path)
              • test_bytes_downloaded_are_recorded(tmp_path)
              • test_valid_checksum_is_verified(tmp_path)
              • test_invalid_checksum_fails(tmp_path)
              • test_missing_destination_fails()
              • test_missing_urls_fails(tmp_path)
              • test_disabled_manifest_is_skipped(tmp_path)
              • test_successful_acquisition_updates_source_status(tmp_path)
              • test_successful_checksum_acquisition_reaches_validated(tmp_path)
              • test_failed_acquisition_updates_source_status(tmp_path)
              • test_result_preserves_source_identity(tmp_path)
              • test_url_filename_is_used_when_expected_filename_missing(tmp_path)
        📄 test_source_acquirer.py
            ⚙️ Functions:
              • test_source_acquirer_is_abstract()
              • test_source_acquirer_cannot_be_instantiated()
        📄 test_source_format.py
            ⚙️ Functions:
              • test_source_format_values()
              • test_text_formats()
              • test_structured_formats()
              • test_archive_formats()
              • test_ocr_formats()
              • test_document_formats()
              • test_from_extension_normalizes_input()
              • test_from_extension_unknown_returns_unknown()
              • test_string_representation()
        📄 test_source_license.py
            ⚙️ Functions:
              • test_license_values()
              • test_open_licenses()
              • test_non_open_licenses()
              • test_attribution_requirements()
              • test_commercial_use()
              • test_permission_required()
              • test_from_string()
              • test_unknown_license()
              • test_string_representation()
        📄 test_source_repository.py
            ⚙️ Functions:
              • make_source(identifier)
              • test_repository_starts_empty()
              • test_add_registers_source()
              • test_add_duplicate_identifier_is_rejected()
              • test_get_returns_registered_source()
              • test_get_returns_none_for_unknown_source()
              • test_exists_returns_false_for_unknown_source()
              • test_exists_returns_true_for_registered_source()
              • test_all_returns_registered_sources()
              • test_all_returns_immutable_snapshot()
              • test_remove_returns_removed_source()
              • test_remove_unknown_returns_none()
              • test_clear_removes_all_sources()
              • test_repository_is_iterable()
              • test_contains_protocol()
              • test_len_protocol()
        📄 test_source_status.py
            ⚙️ Functions:
              • test_initial_statuses()
              • test_downloaded_states()
              • test_validated_states()
              • test_importable_states()
              • test_terminal_states()
              • test_failed_state()
              • test_active_states()
              • test_from_string()
              • test_unknown_status()
              • test_string_representation()
        📄 test_source_type.py
            🏗️ Classes:
              • class TestSourceType:
                - test_from_string(self)
                - test_unknown(self)
                - test_is_reference(self)
                - test_string(self)
        📂 knowledge/
          📄 test_abstract_lexical_manifest.py
              ⚙️ Functions:
                • make_manifest()
                • test_manifest_is_abstract()
                • test_concrete_manifest_is_instantiable()
                • test_identifier_is_required_contract()
                • test_summary_is_required_contract()
                • test_identity_fields_are_preserved()
                • test_default_language_is_sanskrit()
                • test_default_script_is_devanagari()
                • test_default_encoding_is_utf8()
                • test_optional_source_fields_default_to_none()
                • test_optional_local_acquisition_fields_default_to_none()
                • test_optional_publication_fields_default_to_none()
                • test_optional_metadata_defaults_to_none()
                • test_display_name_defaults_to_resource_name()
                • test_has_download_is_false_without_download_url()
                • test_has_download_is_true_with_download_url()
                • test_has_local_copy_is_false_without_local_directory()
                • test_has_local_copy_is_true_with_local_directory()
                • test_manifest_is_frozen()
                • test_manifest_is_slot_based()
                • test_manifest_has_no_instance_dictionary()
                • test_string_representation_contains_class_name()
                • test_string_representation_contains_identifier()
                • test_string_representation_contains_version()
                • test_manifest_accepts_complete_metadata()
              🏗️ Classes:
                • class _ConcreteManifest:
                  - identifier(self)
                  - summary(self)
          📄 test_abstract_lexical_parser.py
              ⚙️ Functions:
                • make_parser()
                • test_parser_is_abstract()
                • test_concrete_parser_is_instantiable()
                • test_identifier_returns_concrete_class_name()
                • test_summary_contains_parser_information()
                • test_string_representation_contains_source()
                • test_iter_records_reads_source_records(tmp_path)
                • test_iter_records_preserves_raw_record_content(tmp_path)
                • test_iter_records_uses_parser_encoding(tmp_path)
                • test_parse_record_creates_raw_lexical_entry()
                • test_parse_record_preserves_source_provenance()
                • test_parse_record_strips_record_for_headword()
                • test_parse_record_ignores_blank_records()
                • test_parse_returns_raw_lexical_entries(tmp_path)
                • test_parse_preserves_record_order(tmp_path)
                • test_parse_skips_blank_records(tmp_path)
                • test_parse_preserves_provenance_for_every_entry(tmp_path)
                • test_parse_assigns_distinct_source_record_ids(tmp_path)
                • test_parser_does_not_normalize_source_word()
                • test_parser_does_not_create_canonical_lexical_objects()
                • test_parser_output_is_immutable()
                • test_parse_missing_source_raises_file_not_found(tmp_path)
                • test_parse_empty_source_returns_empty_tuple(tmp_path)
                • test_parser_is_slot_based()
                • test_parser_has_expected_configuration()
              🏗️ Classes:
                • class _ConcreteParser:
                  - parse(self, source)
                  - iter_records(self, source)
                  - parse_record(self, record)
          📄 test_abstract_lexical_repository.py
              ⚙️ Functions:
                • make_repository(**overrides)
                • make_record(headword)
                • test_abstract_repository_cannot_be_instantiated()
                • test_concrete_repository_can_be_instantiated()
                • test_repository_name_is_preserved()
                • test_default_repository_version_is_applied()
                • test_custom_repository_version_is_preserved()
                • test_identifier_alias_returns_repository_name()
                • test_add_inserts_one_record()
                • test_add_all_inserts_every_record()
                • test_add_all_accepts_any_iterable()
                • test_get_returns_matching_headword_records()
                • test_get_returns_empty_tuple_for_missing_headword()
                • test_contains_is_true_for_existing_headword()
                • test_contains_is_false_for_missing_headword()
                • test_all_returns_all_records_in_insertion_order()
                • test_clear_removes_all_records()
                • test_clear_on_empty_repository_is_safe()
                • test_iteration_delegates_to_all()
                • test_len_delegates_to_count()
                • test_summary_contains_repository_diagnostics()
                • test_string_representation_contains_record_count()
              🏗️ Classes:
                • class DummyRepository:
                  - __init__(self, repository_name, repository_version)
                  - add(self, record)
                  - get(self, headword)
                  - contains(self, headword)
                  - all(self)
                  - clear(self)
                  - count(self)
          📄 test_abstract_lexical_transformer.py
              ⚙️ Functions:
                • make_transformer(**overrides)
                • make_entry(headword)
                • test_abstract_transformer_cannot_be_instantiated()
                • test_concrete_transformer_can_be_instantiated()
                • test_resource_name_is_preserved()
                • test_default_resource_version_is_unknown()
                • test_custom_resource_version_is_preserved()
                • test_identifier_defaults_to_concrete_class_name()
                • test_transform_returns_canonical_lexical_record()
                • test_transform_preserves_headword_for_multiple_entries()
                • test_transform_all_returns_tuple()
                • test_transform_all_preserves_input_order()
                • test_transform_all_accepts_generators()
                • test_transform_all_empty_input_returns_empty_tuple()
                • test_summary_contains_transformer_diagnostics()
                • test_string_representation_contains_class_and_resource()
              🏗️ Classes:
                • class DummyTransformer:
                  - __init__(self, resource_name, resource_version)
                  - transform(self, entry)
          📂 monier_williams/
            📄 test_delimited_monier_williams_parser.py
                ⚙️ Functions:
                  • test_parser_reads_basic_record()
                  • test_parser_reads_optional_fields()
                  • test_parser_rejects_invalid_header()
                  • test_parser_empty_source_returns_empty_tuple()
                  • test_parser_whitespace_only_source_returns_empty_tuple()
                  • test_parser_returns_monier_williams_records()
                  • test_parser_sets_source_to_monier_williams()
            📄 test_file_monier_williams_source.py
                ⚙️ Functions:
                  • test_file_source_reads_text(tmp_path)
                  • test_file_source_identifier()
                  • test_file_source_name()
                  • test_file_source_exposes_path()
                  • test_file_source_missing_file(tmp_path)
                  • test_file_source_rejects_directory(tmp_path)
            📄 test_local_monier_williams_source_acquirer.py
                ⚙️ Functions:
                  • test_local_acquirer_reads_source(tmp_path)
                  • test_local_acquirer_exposes_path(tmp_path)
                  • test_local_acquirer_rejects_missing_file(tmp_path)
                  • test_local_acquirer_rejects_directory(tmp_path)
            📄 test_monier_williams_acquisition_service.py
                ⚙️ Functions:
                  • test_acquisition_service_reads_source()
                  • test_acquisition_service_returns_counts()
                  • test_acquisition_service_read_is_convenience_method()
                  • test_source_is_not_replaced()
                🏗️ Classes:
                  • class StubSource:
                    - __init__(self, text)
                    - identifier(self)
                    - source_name(self)
                    - read(self)
            📄 test_monier_williams_compatibility.py
                ⚙️ Functions:
                  • test_parser_accepts_extended_canonical_headers()
                  • test_parser_empty_source_returns_empty_tuple()
                  • test_parser_supports_custom_delimiter()
                  • test_parser_supports_parse_lines()
                  • test_file_source_exposes_source(tmp_path)
                  • test_lightweight_source_double_is_valid()
                  • test_source_parser_accepts_injected_acquirer()
                  • test_source_parser_accepts_custom_parser()
                🏗️ Classes:
                  • class StubSource:
                    - __init__(self, text)
                    - acquire(self)
            📄 test_monier_williams_parsed_entry.py
                ⚙️ Functions:
                  • test_parsed_entry_stores_required_fields()
                  • test_parsed_entry_stores_optional_fields()
                  • test_empty_headword_is_rejected()
                  • test_empty_definition_is_rejected()
                  • test_metadata_is_immutable()
            📄 test_monier_williams_parser.py
                ⚙️ Functions:
                  • test_parse_lines_delegates_to_parse()
            📄 test_monier_williams_source_parser.py
                🔹 Constants:
                  • MW_SAMPLE
                ⚙️ Functions:
                  • test_parser_reads_multiple_records()
                  • test_parser_reads_headword()
                  • test_parser_reads_homonym()
                  • test_parser_preserves_grammatical_field()
                  • test_parser_preserves_definition_field()
                  • test_parser_preserves_raw_record()
                  • test_parser_rejects_empty_source()
                  • test_parser_rejects_unterminated_record()
                  • test_parser_rejects_orphan_lend()
                  • test_parser_rejects_source_without_records()
                  • test_parse_record_requires_one_record()
            📄 test_monier_williams_source_pipeline.py
                ⚙️ Functions:
                  • test_pipeline_acquires_and_parses()
                🏗️ Classes:
                  • class StubSource:
                    - identifier(self)
                    - source_name(self)
                    - read(self)
            📄 test_monier_williams_source_record.py
                ⚙️ Functions:
                  • test_source_record_exposes_fields()
                  • test_source_record_unknown_field_is_preserved()
                  • test_source_record_requires_positive_sequence()
                  • test_source_record_requires_raw_text()
      📂 core/
        📄 test_typing.py
            ⚙️ Functions:
              • test_generic_type_variables_exist()
              • test_tobject_is_exported()
              • test_tobject_is_unconstrained()
              • test_json_aliases_exist()
              • test_path_like_accepts_string_and_path()
              • test_attributes_is_dictionary()
              • test_collection_aliases_are_available()
              • test_callable_aliases_are_available()
              • test_all_expected_symbols_are_exported()
              • test_json_dict_accepts_json_compatible_values()
        📂 validators/
          📄 test_composite_validator.py
              ⚙️ Functions:
                • test_empty_composite_is_valid()
                • test_valid_object_passes_all_validators()
                • test_invalid_object_reports_issue()
                • test_multiple_validators_are_aggregated()
                • test_unsupported_validator_is_not_executed()
                • test_validator_order_is_preserved()
                • test_validate_many_aggregates_results()
              🏗️ Classes:
                • class DummyObject:
                • class IdentifierValidator:
                  - supports(cls, obj)
                  - validate(self, obj)
                • class AlwaysErrorValidator:
                  - supports(cls, obj)
                  - validate(self, obj)
                • class UnsupportedValidator:
                  - supports(cls, obj)
                  - validate(self, obj)
          📄 test_validation_issue.py
              ⚙️ Functions:
                • test_validation_severity_defines_expected_values()
                • test_validation_severity_is_string_enum()
                • test_validation_issue_can_be_created_with_required_fields()
                • test_validation_issue_defaults_to_error()
                • test_validation_issue_accepts_warning()
                • test_validation_issue_accepts_info()
                • test_validation_issue_supports_field()
                • test_validation_issue_supports_location()
                • test_validation_issue_supports_suggestion()
                • test_validation_issue_optional_fields_default_to_empty_strings()
                • test_validation_issue_is_frozen()
                • test_validation_issue_is_hashable()
                • test_validation_issues_with_same_values_are_equal()
                • test_validation_issues_with_different_codes_are_not_equal()
                • test_validation_issue_severity_predicates_are_mutually_consistent()
          📄 test_validation_result.py
              ⚙️ Functions:
                • make_info_issue()
                • make_warning_issue()
                • make_error_issue()
                • test_default_result_is_successful()
                • test_success_creates_empty_result()
                • test_from_issues_accepts_iterable()
                • test_from_issues_accepts_generator()
                • test_result_with_info_only_is_valid()
                • test_result_with_warning_only_is_valid()
                • test_result_with_error_is_invalid()
                • test_result_detects_all_severities()
                • test_error_count()
                • test_warning_count()
                • test_info_count()
                • test_counts_are_zero_when_no_matching_issue_exists()
                • test_errors_returns_only_errors()
                • test_warnings_returns_only_warnings()
                • test_info_returns_only_info_issues()
                • test_filtering_preserves_original_order()
                • test_merge_combines_issues()
                • test_merge_preserves_order()
                • test_merge_does_not_modify_original_results()
                • test_bool_is_true_for_valid_result()
                • test_bool_is_false_for_invalid_result()
                • test_len_returns_number_of_issues()
                • test_validation_result_is_frozen()
                • test_issues_are_stored_as_tuple()
                • test_equal_results_are_equal()
                • test_results_with_different_issues_are_not_equal()
          📄 test_validator.py
              ⚙️ Functions:
                • test_validator_is_abstract()
                • test_validator_cannot_be_instantiated_directly()
                • test_validate_is_abstract()
                • test_concrete_validator_can_be_instantiated()
                • test_validate_returns_validation_result()
                • test_valid_object_returns_success()
                • test_invalid_object_returns_error()
                • test_validate_many_with_empty_iterable_returns_success()
                • test_validate_many_validates_all_objects()
                • test_validate_many_accepts_generator()
                • test_validate_many_merges_validation_results()
                • test_validate_many_preserves_validation_order()
                • test_validate_many_calls_validate_once_per_object()
                • test_validate_many_returns_single_merged_result()
                • test_validate_many_preserves_issue_order()
                • test_default_supports_returns_true()
                • test_supports_is_class_method()
                • test_supports_accepts_arbitrary_object()
                • test_concrete_validator_inherits_default_supports()
                • test_supports_can_be_overridden()
                • test_validator_generic_contract_accepts_typed_objects()
              🏗️ Classes:
                • class StubValidator:
                  - validate(self, obj)
                • class RecordingValidator:
                  - __init__(self)
                  - validate(self, obj)
                • class SelectiveValidator:
                  - validate(self, obj)
          📄 test_validator_registry.py
              ⚙️ Functions:
                • test_empty_registry_is_empty()
                • test_register_validator()
                • test_registered_validator_can_be_retrieved()
                • test_missing_validator_returns_none()
                • test_supporting_returns_matching_validators()
                • test_supporting_preserves_registration_order()
                • test_duplicate_registration_is_rejected()
              🏗️ Classes:
                • class DummyValidator:
                  - __init__(self, supported_type)
                  - supports(cls, obj)
                  - validate(self, obj)
                • class StringValidator:
                  - supports(cls, obj)
                  - validate(self, obj)
                • class IntegerValidator:
                  - supports(cls, obj)
                  - validate(self, obj)
      📂 corpus/
        📄 __init__.py
        📄 test_corpus_navigation_structure.py
            ⚙️ Functions:
              • test_canonical_corpus_hierarchy_navigation()
              • test_canonical_order_is_preserved()
        📂 builders/
          📄 test_base_builder.py
              ⚙️ Functions:
                • test_base_builder_is_abstract()
                • test_concrete_builder_creates_initial_instance()
                • test_instance_returns_current_working_instance()
                • test_reset_creates_fresh_instance()
                • test_reset_allows_builder_reuse()
                • test_build_returns_constructed_object()
                • test_build_returns_deep_copy()
                • test_build_does_not_disconnect_builder_from_working_instance()
                • test_default_validate_succeeds()
                • test_build_calls_validation()
                • test_validating_builder_builds_valid_instance()
                • test_is_valid_returns_true_when_validation_succeeds()
                • test_is_valid_returns_false_when_validation_fails()
                • test_from_instance_copies_existing_object()
                • test_from_instance_performs_deep_copy()
                • test_from_instance_returns_builder_for_fluent_use()
                • test_clone_returns_same_builder_type()
                • test_clone_copies_current_instance()
                • test_clone_performs_deep_copy()
                • test_builder_lifecycle_is_fluent()
              🏗️ Classes:
                • class DummyObject:
                  - __post_init__(self)
                • class DummyBuilder:
                  - _create_instance(self)
                • class ValidatingDummyBuilder:
                  - _create_instance(self)
                  - validate(self)
          📄 test_child_node_builder.py
              ⚙️ Functions:
                • test_child_node_builder_creates_parent_instance()
                • test_add_child_adds_single_child()
                • test_add_child_preserves_child_identity()
                • test_add_multiple_single_children_preserves_order()
                • test_add_children_adds_all_children()
                • test_add_children_preserves_input_order()
                • test_add_children_accepts_empty_iterable()
                • test_add_children_accepts_generator()
                • test_child_operations_are_fluent()
                • test_child_node_builder_inherits_node_validation()
                • test_reset_removes_existing_children()
                • test_build_returns_independent_parent_with_children()
                • test_build_deep_copies_children()
                • test_from_instance_preserves_children()
                • test_from_instance_copies_children_independently()
              🏗️ Classes:
                • class DummyMetadata:
                • class DummyChild:
                  - __init__(self, identifier, title)
                • class DummyContainer:
                  - __init__(self)
                  - add_child(self, child)
                • class DummyChildNodeBuilder:
                  - _create_instance(self)
                  - add_child(self, child)
                  - add_children(self, children)
          📄 test_corpus_builder.py
              ⚙️ Functions:
                • test_create_instance_returns_corpus()
                • test_create_instance_generates_corpus_id()
                • test_create_instance_initializes_corpus_metadata()
                • test_with_title_is_fluent()
                • test_with_description_is_fluent()
                • test_with_metadata_is_fluent()
                • test_with_title_sets_metadata_title()
                • test_with_description_sets_metadata_description()
                • test_with_metadata_replaces_metadata()
                • test_add_document_is_fluent()
                • test_add_document_adds_document()
                • test_add_documents_adds_all_documents()
                • test_validate_accepts_non_empty_title()
                • test_validate_rejects_empty_title()
                • test_validate_rejects_whitespace_title()
                • test_build_requires_valid_title()
                • test_build_returns_corpus()
                • test_build_returns_independent_copy()
                • test_build_does_not_replace_builder_instance()
                • test_reset_creates_fresh_corpus()
                • test_reset_clears_previous_metadata()
                • test_from_corpus_returns_corpus_builder()
                • test_from_corpus_copies_corpus_state()
                • test_from_corpus_preserves_documents()
                • test_from_corpus_does_not_alias_original_corpus()
          📄 test_corpus_builder_integration.py
              ⚙️ Functions:
                • make_token(text, sequence)
                • make_line(sequence, tokens)
                • make_paragraph(number, lines)
                • make_verse(number, paragraphs)
                • make_section(title, number, verses)
                • make_document(title, sections)
                • make_corpus(title, documents)
                • test_complete_hierarchy_can_be_constructed()
                • test_complete_hierarchy_preserves_order()
                • test_complete_hierarchy_supports_multiple_children()
                • test_builders_can_be_composed_fluently()
                • test_build_returns_independent_snapshot()
                • test_build_snapshot_does_not_alias_builder_instance()
                • test_corpus_builder_reset_clears_complete_hierarchy()
                • test_separate_corpus_builders_generate_distinct_identifiers()
                • test_complete_hierarchy_serializes_recursively()
                • test_corpus_builder_rejects_empty_title()
                • test_complete_hierarchy_counts_are_consistent()
          📄 test_document_builder.py
              ⚙️ Functions:
                • make_section(title)
                • test_create_instance_returns_document()
                • test_create_instance_initializes_metadata()
                • test_create_instance_generates_identifier()
                • test_with_title_is_fluent()
                • test_with_document_type_sets_metadata()
                • test_with_page_range_sets_metadata()
                • test_with_publisher_sets_metadata()
                • test_with_edition_sets_metadata()
                • test_with_publication_year_sets_metadata()
                • test_add_author()
                • test_add_editor()
                • test_add_translator()
                • test_add_section()
                • test_add_sections_preserves_order()
                • test_build_returns_independent_copy()
                • test_reset_creates_fresh_document()
                • test_from_document_returns_document_builder()
                • test_from_document_does_not_alias_original()
          📄 test_line_builder.py
              ⚙️ Functions:
                • make_line(number)
                • make_token(text, position)
                • test_create_instance_returns_line()
                • test_create_instance_initializes_metadata()
                • test_create_instance_generates_identifier()
                • test_with_line_number_is_fluent()
                • test_with_line_number_sets_metadata()
                • test_with_visual_line_number_is_fluent()
                • test_with_visual_line_number_sets_metadata()
                • test_with_visual_line_number_accepts_none()
                • test_with_pada_number_is_fluent()
                • test_with_pada_number_sets_metadata()
                • test_with_pada_number_accepts_none()
                • test_with_indentation_is_fluent()
                • test_with_indentation_sets_metadata()
                • test_as_continuation_is_fluent()
                • test_as_continuation_sets_metadata()
                • test_as_continuation_accepts_false()
                • test_add_token_is_fluent()
                • test_add_token_adds_child()
                • test_add_tokens_adds_all_children()
                • test_add_tokens_preserves_order()
                • test_build_returns_independent_copy()
                • test_reset_creates_fresh_line()
                • test_reset_clears_tokens()
                • test_from_line_returns_builder()
                • test_from_line_copies_metadata()
                • test_from_line_does_not_alias_original()
          📄 test_node_builder.py
              ⚙️ Functions:
                • test_node_builder_creates_node()
                • test_node_builder_creates_fresh_node()
                • test_with_metadata_replaces_metadata()
                • test_with_title_sets_title()
                • test_with_description_sets_description()
                • test_with_identifier_sets_metadata_identifier()
                • test_with_identifier_does_not_change_node_id()
                • test_with_sequence_number_sets_sequence_number()
                • test_with_sequence_number_accepts_none()
                • test_with_parent_identifier_sets_parent()
                • test_metadata_methods_are_fluent()
                • test_empty_title_is_invalid()
                • test_whitespace_only_title_is_invalid()
                • test_non_empty_title_is_valid()
                • test_is_valid_reflects_title_validation()
                • test_build_valid_node()
                • test_build_returns_independent_node()
                • test_reset_restores_fresh_node()
                • test_from_instance_preserves_node_data()
                • test_from_instance_is_independent_from_source()
              🏗️ Classes:
                • class DummyMetadata:
                • class DummyNode:
                  - __init__(self, identifier, metadata)
                • class DummyNodeBuilder:
                  - _create_instance(self)
          📄 test_paragraph_builder.py
              ⚙️ Functions:
                • make_paragraph(number)
                • make_line(number)
                • first_enum_member(enum_class)
                • test_create_instance_returns_paragraph()
                • test_create_instance_initializes_metadata()
                • test_create_instance_generates_identifier()
                • test_with_paragraph_number_is_fluent()
                • test_with_paragraph_number_sets_metadata()
                • test_with_paragraph_type_is_fluent()
                • test_with_paragraph_type_sets_metadata()
                • test_with_language_variant_is_fluent()
                • test_with_language_variant_sets_metadata()
                • test_as_translation_is_fluent()
                • test_as_translation_sets_metadata()
                • test_as_translation_accepts_false()
                • test_as_commentary_is_fluent()
                • test_as_commentary_sets_metadata()
                • test_as_commentary_accepts_false()
                • test_add_line_is_fluent()
                • test_add_line_adds_child()
                • test_add_lines_adds_all_children()
                • test_add_lines_preserves_order()
                • test_build_returns_independent_copy()
                • test_reset_creates_fresh_paragraph()
                • test_reset_clears_lines()
                • test_from_paragraph_returns_builder()
                • test_from_paragraph_copies_metadata()
                • test_from_paragraph_does_not_alias_original()
          📄 test_section_builder.py
              ⚙️ Functions:
                • make_verse(number)
                • make_section(title)
                • test_create_instance_returns_section()
                • test_create_instance_initializes_metadata()
                • test_create_instance_generates_identifier()
                • test_with_title_is_fluent()
                • test_with_title_sets_metadata()
                • test_with_section_type_is_fluent()
                • test_with_section_type_sets_metadata()
                • test_with_section_number_is_fluent()
                • test_with_section_number_maps_to_numbering_scheme()
                • test_add_verse_is_fluent()
                • test_add_verse_adds_verse()
                • test_add_verses_adds_all_verses()
                • test_add_verses_preserves_order()
                • test_build_returns_section()
                • test_build_returns_independent_copy()
                • test_reset_creates_fresh_section()
                • test_reset_clears_verses()
                • test_from_section_returns_section_builder()
                • test_from_section_copies_metadata()
                • test_from_section_does_not_alias_original()
          📄 test_token_builder.py
              ⚙️ Functions:
                • first_enum_member(enum_class)
                • test_create_instance_returns_token()
                • test_create_instance_initializes_metadata()
                • test_create_instance_generates_identifier()
                • test_with_text_is_fluent()
                • test_with_text_sets_metadata()
                • test_with_normalized_text_is_fluent()
                • test_with_normalized_text_sets_metadata()
                • test_with_position_is_fluent()
                • test_with_position_sets_metadata()
                • test_with_token_type_is_fluent()
                • test_with_token_type_sets_metadata()
                • test_with_confidence_is_fluent()
                • test_with_confidence_sets_metadata()
                • test_with_source_offset_is_fluent()
                • test_with_source_offset_sets_metadata()
                • test_build_returns_independent_copy()
                • test_reset_creates_fresh_token()
                • test_from_token_returns_builder()
                • test_from_token_copies_metadata()
                • test_from_token_does_not_alias_original()
          📄 test_verse_builder.py
              ⚙️ Functions:
                • make_verse(number)
                • make_paragraph(number)
                • first_enum_member(enum_class)
                • test_create_instance_returns_verse()
                • test_create_instance_initializes_metadata()
                • test_create_instance_generates_identifier()
                • test_with_verse_number_is_fluent()
                • test_with_verse_number_sets_metadata()
                • test_with_verse_type_is_fluent()
                • test_with_verse_type_sets_metadata()
                • test_with_meter_is_fluent()
                • test_with_meter_sets_metadata()
                • test_with_meter_name_is_fluent()
                • test_with_meter_name_sets_metadata()
                • test_add_paragraph_is_fluent()
                • test_add_paragraph_adds_child()
                • test_add_paragraphs_adds_all_children()
                • test_add_paragraphs_preserves_order()
                • test_build_returns_independent_copy()
                • test_reset_creates_fresh_verse()
                • test_reset_clears_paragraphs()
                • test_from_verse_returns_verse_builder()
                • test_from_verse_copies_metadata()
                • test_from_verse_does_not_alias_original()
        📂 models/
          📄 test_base_node.py
              ⚙️ Functions:
                • test_base_node_can_be_used_through_concrete_subclass()
                • test_identifier_is_stored()
                • test_identifier_property_is_alias_for_id()
                • test_metadata_is_stored()
                • test_base_node_supports_non_string_identifier()
                • test_base_node_preserves_identifier_value()
                • test_nodes_with_same_type_and_identifier_are_equal()
                • test_nodes_with_different_identifiers_are_not_equal()
                • test_nodes_with_same_identifier_but_different_types_are_not_equal()
                • test_node_is_not_equal_to_unrelated_object()
                • test_nodes_with_same_type_and_identifier_have_same_hash()
                • test_nodes_with_different_identifiers_have_different_hashes()
                • test_node_can_be_used_as_set_member()
                • test_equal_nodes_resolve_to_same_set_member()
                • test_repr_contains_class_name()
                • test_repr_contains_identifier()
                • test_repr_follows_expected_base_node_format()
                • test_metadata_does_not_participate_in_equality()
                • test_metadata_does_not_participate_in_hash()
                • test_id_and_identifier_are_consistent()
                • test_identifier_is_read_only_property()
                • test_id_is_read_only_property()
                • test_base_node_contract_is_stable()
              🏗️ Classes:
                • class NodeMetadata:
                • class ConcreteNode:
                • class OtherConcreteNode:
          📄 test_container_node_contract.py
              🔹 Constants:
                • CONTAINER_CONTRACTS
              ⚙️ Functions:
                • make_document(identifier)
                • make_section(identifier)
                • make_verse(identifier)
                • make_paragraph(identifier)
                • make_line(identifier)
                • make_token(identifier)
                • test_structural_nodes_are_container_nodes(node_class, make_parent, make_child, children_property, add_method, remove_method, count_property, first_property, last_property)
                • test_container_starts_empty(node_class, make_parent, make_child, children_property, add_method, remove_method, count_property, first_property, last_property)
                • test_container_adds_child(node_class, make_parent, make_child, children_property, add_method, remove_method, count_property, first_property, last_property)
                • test_container_preserves_insertion_order(node_class, make_parent, make_child, children_property, add_method, remove_method, count_property, first_property, last_property)
                • test_container_is_iterable(node_class, make_parent, make_child, children_property, add_method, remove_method, count_property, first_property, last_property)
                • test_container_extend(node_class, make_parent, make_child, children_property, add_method, remove_method, count_property, first_property, last_property)
                • test_container_remove_child(node_class, make_parent, make_child, children_property, add_method, remove_method, count_property, first_property, last_property)
                • test_container_clear_children(node_class, make_parent, make_child, children_property, add_method, remove_method, count_property, first_property, last_property)
                • test_domain_children_alias_is_same_collection(node_class, make_parent, make_child, children_property, add_method, remove_method, count_property, first_property, last_property)
          📄 test_corpus.py
              ⚙️ Functions:
                • make_corpus(identifier)
                • make_document(identifier)
                • test_corpus_stores_identifier()
                • test_corpus_identifier_aliases_id()
                • test_corpus_stores_metadata()
                • test_corpus_is_a_container_node()
                • test_corpus_uses_container_node_children()
                • test_documents_alias_children()
                • test_corpus_starts_without_documents()
                • test_document_count_aliases_child_count()
                • test_add_document()
                • test_remove_document()
                • test_clear_documents()
                • test_first_document_aliases_first_child()
                • test_last_document_aliases_last_child()
                • test_first_and_last_document_are_none_when_empty()
                • test_documents_preserve_insertion_order()
                • test_children_preserve_same_insertion_order_as_documents()
                • test_corpus_supports_iteration()
                • test_corpus_supports_indexing()
                • test_corpus_length_aliases_document_count()
                • test_corpus_id_is_read_only()
                • test_corpus_identifier_is_read_only()
                • test_corpus_identity_is_type_safe()
                • test_corpus_different_identifiers_are_not_equal()
                • test_corpus_repr_contains_identifier()
                • test_corpus_repr_contains_document_count()
          📄 test_corpus_metadata.py
              ⚙️ Functions:
                • test_default_construction()
                • test_to_dict_returns_dict()
                • test_to_dict_contains_metadata_fields()
                • test_repr_is_available()
          📄 test_document.py
              ⚙️ Functions:
                • make_document(identifier)
                • make_section(identifier)
                • test_document_stores_identifier()
                • test_document_stores_metadata()
                • test_document_starts_without_sections()
                • test_sections_alias_children()
                • test_add_section()
                • test_remove_section()
                • test_first_section()
                • test_last_section()
                • test_sections_preserve_insertion_order()
          📄 test_document_metadata.py
              ⚙️ Functions:
                • test_default_construction()
                • test_to_dict_returns_dict()
                • test_to_dict_contains_metadata_fields()
                • test_repr_is_available()
          📄 test_line.py
              ⚙️ Functions:
                • make_line(identifier)
                • make_token(identifier, text)
                • test_line_stores_identifier()
                • test_line_stores_metadata()
                • test_line_starts_without_tokens()
                • test_tokens_alias_children()
                • test_add_token()
                • test_remove_token()
                • test_first_token()
                • test_last_token()
                • test_tokens_preserve_insertion_order()
                • test_line_number_aliases_metadata()
                • test_language_aliases_metadata()
          📄 test_line_metadata.py
              ⚙️ Functions:
                • test_default_construction()
                • test_default_language_is_sanskrit()
                • test_language_can_be_specified()
                • test_to_dict_returns_dict()
                • test_to_dict_contains_language()
                • test_repr_is_available()
          📄 test_paragraph.py
              ⚙️ Functions:
                • make_paragraph(identifier)
                • make_line(identifier)
                • test_paragraph_stores_identifier()
                • test_paragraph_stores_metadata()
                • test_paragraph_starts_without_lines()
                • test_lines_alias_children()
                • test_add_line()
                • test_remove_line()
                • test_first_line()
                • test_last_line()
                • test_lines_preserve_insertion_order()
          📄 test_paragraph_metadata.py
              ⚙️ Functions:
                • test_default_construction()
                • test_to_dict_returns_dict()
                • test_to_dict_contains_metadata_fields()
                • test_repr_is_available()
          📄 test_section.py
              ⚙️ Functions:
                • make_section(identifier)
                • make_verse(identifier)
                • test_section_stores_identifier()
                • test_section_stores_metadata()
                • test_section_starts_without_verses()
                • test_verses_alias_children()
                • test_add_verse()
                • test_remove_verse()
                • test_first_verse()
                • test_last_verse()
                • test_verses_preserve_insertion_order()
          📄 test_section_metadata.py
              ⚙️ Functions:
                • test_default_construction()
                • test_to_dict_returns_dict()
                • test_to_dict_contains_metadata_fields()
                • test_repr_is_available()
          📄 test_token.py
              ⚙️ Functions:
                • make_token(identifier, text, normalized_text)
                • test_token_stores_identifier()
                • test_token_stores_metadata()
                • test_token_is_a_base_node()
                • test_token_is_leaf_node()
                • test_token_text_aliases_metadata()
                • test_token_normalized_text_aliases_metadata()
                • test_token_preserves_original_and_normalized_text()
                • test_token_metadata_is_accessible()
          📄 test_token_metadata.py
              ⚙️ Functions:
                • test_default_construction()
                • test_to_dict_returns_dict()
                • test_to_dict_contains_metadata_fields()
                • test_repr_is_available()
          📄 test_verse.py
              ⚙️ Functions:
                • make_verse(identifier)
                • make_paragraph(identifier)
                • test_verse_stores_identifier()
                • test_verse_stores_metadata()
                • test_verse_starts_without_paragraphs()
                • test_paragraphs_alias_children()
                • test_add_paragraph()
                • test_remove_paragraph()
                • test_first_paragraph()
                • test_last_paragraph()
                • test_paragraphs_preserve_insertion_order()
          📄 test_verse_metadata.py
              ⚙️ Functions:
                • test_default_construction()
                • test_to_dict_returns_dict()
                • test_to_dict_contains_metadata_fields()
                • test_repr_is_available()
      📂 domain/
        📄 __init__.py
        📂 derivation/
          📄 test_derivation_rule_set.py
              ⚙️ Functions:
                • test_empty_rule_set_has_no_rules()
                • test_rule_set_accepts_rules()
                • test_apply_returns_no_candidates_for_empty_rule_set()
                • test_apply_checks_every_rule()
                • test_apply_only_applies_matching_rules()
                • test_apply_preserves_rule_order()
                • test_apply_preserves_candidate_order_within_rules()
                • test_apply_removes_duplicate_hashable_candidates()
                • test_apply_supports_unhashable_candidates()
                • test_apply_preserves_first_occurrence_of_unhashable_candidates()
                • test_apply_does_not_duplicate_identical_candidates_from_multiple_rules()
                • test_apply_does_not_mutate_rule_set()
                • test_apply_can_be_called_multiple_times()
                • test_apply_does_not_retain_previous_candidates()
                • test_non_matching_rules_are_not_applied_even_when_other_rules_match()
              🏗️ Classes:
                • class FakeContext:
                • class FakeRule:
                  - __init__(self)
                  - identifier(self)
                  - applies_to(self, context)
                  - apply(self, context)
        📂 dhatu/
          📄 test_default_dhatu_repository.py
              ⚙️ Functions:
                • make_dhatu(identifier, root, gana, transliteration, meaning, notes)
              🏗️ Classes:
                • class TestDefaultDhatuRepository:
                  - test_can_be_created_empty(self)
                  - test_accepts_initial_dhatus(self)
                  - test_get_unknown_returns_none(self)
                  - test_contains_identifier(self)
                  - test_find_by_root(self)
                  - test_find_by_root_unknown_returns_empty(self)
                  - test_find_by_gana(self)
                  - test_find_by_gana_unknown_returns_empty(self)
                  - test_search_by_identifier(self)
                  - test_search_by_root(self)
                  - test_search_by_transliteration(self)
                  - test_search_by_meaning(self)
                  - test_search_by_notes(self)
                  - test_search_by_gana_name(self)
                  - test_search_is_case_insensitive_for_latin_fields(self)
                  - test_empty_search_returns_empty(self)
                  - test_unknown_search_returns_empty(self)
                  - test_all_returns_insertion_order(self)
                  - test_register_adds_dhatu(self)
                  - test_register_replaces_same_identifier(self)
                  - test_register_many(self)
                  - test_register_rejects_none(self)
                  - test_register_rejects_wrong_type(self)
                  - test_register_rejects_empty_identifier(self)
                  - test_register_rejects_empty_root(self)
                  - test_remove_existing(self)
                  - test_remove_unknown_returns_false(self)
                  - test_clear(self)
          📄 test_default_dhatu_service.py
              🏗️ Classes:
                • class TestDefaultDhatuService:
                  - test_creates_default_service(self)
                  - test_default_resolver_is_created(self)
                  - test_display_name(self)
                  - test_display_text(self)
                  - test_display_description(self)
                  - test_delegates_analysis_to_resolver(self)
                  - test_resolve_is_alias_for_analyze(self)
                  - test_service_is_immutable(self)
                  - test_string_representation(self)
          📄 test_dhatu_service.py
              🏗️ Classes:
                • class TestDhatuService:
                  - test_service_can_be_created(self)
                  - test_display_name(self)
                  - test_display_text(self)
                  - test_display_description(self)
                  - test_analyze_delegates_to_resolver(self)
                  - test_resolve_is_alias_for_analyze(self)
                  - test_service_is_immutable(self)
                  - test_string_representation(self)
        📂 knowledge_graph/
          📄 test_default_knowledge_graph_resolver.py
              ⚙️ Functions:
                • test_default_resolver_is_knowledge_graph_resolver()
                • test_default_resolver_can_be_created()
                • test_default_resolver_uses_default_strategy()
                • test_default_resolver_analyze_returns_result()
                • test_default_resolver_preserves_context()
                • test_default_resolver_display_name()
                • test_default_resolver_display_text()
                • test_default_resolver_display_description()
          📄 test_default_knowledge_graph_strategy.py
              ⚙️ Functions:
                • test_default_strategy_is_knowledge_graph_strategy()
                • test_default_strategy_can_be_created()
                • test_default_strategy_has_expected_display_name()
                • test_default_strategy_has_expected_display_text()
                • test_default_strategy_has_expected_description()
                • test_default_strategy_analyze_returns_result()
                • test_default_strategy_preserves_context()
                • test_default_strategy_result_is_not_none()
          📄 test_knowledge_graph.py
              ⚙️ Functions:
                • node(identifier, label)
                • edge(identifier, relation, source, target)
                • test_empty_graph_can_be_created()
                • test_graph_defaults_are_applied()
                • test_empty_graph_reports_correct_state()
                • test_graph_display_name_uses_label()
                • test_graph_display_name_has_default()
                • test_graph_display_text_matches_display_name()
                • test_graph_display_description_returns_description()
                • test_get_node_returns_matching_node()
                • test_get_node_returns_none_when_missing()
                • test_get_edge_returns_matching_edge()
                • test_get_edge_returns_none_when_missing()
                • test_add_node_returns_new_graph()
                • test_add_node_preserves_existing_graph_data()
                • test_duplicate_node_is_not_added()
                • test_add_edge_adds_missing_source_and_target_nodes()
                • test_add_edge_preserves_existing_nodes()
                • test_duplicate_edge_is_not_added()
                • test_graph_is_iterable_over_nodes()
                • test_graph_len_returns_node_count()
                • test_graph_supports_index_access()
                • test_merge_combines_nodes_and_edges()
                • test_merge_does_not_duplicate_existing_nodes()
                • test_merge_does_not_duplicate_existing_edges()
                • test_merge_metadata_uses_other_graph_values_for_overlapping_keys()
                • test_merge_preserves_first_label_when_present()
                • test_merge_uses_other_label_when_first_is_empty()
                • test_merge_preserves_first_description_when_present()
                • test_merge_uses_other_description_when_first_is_empty()
                • test_graph_is_immutable()
                • test_graph_is_slot_based()
          📄 test_knowledge_graph_builder.py
              ⚙️ Functions:
                • test_builder_can_be_created()
                • test_builder_is_displayable()
                • test_builder_display_name()
                • test_builder_display_text()
                • test_builder_display_description()
                • test_builder_string_representation()
                • test_builder_is_slot_based()
                • test_builder_from_semantic_collection_empty()
                • test_builder_from_chandas_empty()
                • test_builder_from_alankara_empty()
                • test_builder_from_derivation_empty()
                • test_semantic_collection_creates_analysis_nodes()
                • test_chandas_collection_creates_nodes()
                • test_alankara_collection_creates_nodes()
                • test_semantic_analysis_identifiers_are_sequential()
                • test_builder_preserves_confidence()
          📄 test_knowledge_graph_context.py
              ⚙️ Functions:
                • test_context_can_be_created()
                • test_context_defaults()
                • test_context_accepts_metadata()
                • test_context_get_supports_default()
                • test_context_display_name()
                • test_context_display_text_uses_subject()
                • test_context_display_description()
                • test_context_is_immutable()
                • test_context_is_slot_based()
          📄 test_knowledge_graph_diagnostic.py
              ⚙️ Functions:
                • test_diagnostic_can_be_created()
                • test_diagnostic_defaults()
                • test_info_diagnostic()
                • test_warning_diagnostic()
                • test_error_diagnostic()
                • test_severity_checks_are_case_insensitive()
                • test_diagnostic_display_name()
                • test_diagnostic_display_text()
                • test_diagnostic_display_description()
                • test_diagnostic_is_immutable()
                • test_diagnostic_is_slot_based()
          📄 test_knowledge_graph_edge.py
              ⚙️ Functions:
                • make_source()
                • make_target()
                • make_edge()
                • test_edge_can_be_created()
                • test_edge_defaults_are_applied()
                • test_edge_accepts_full_metadata()
                • test_display_name_returns_relation()
                • test_display_text_contains_source_relation_and_target()
                • test_display_description_returns_description()
                • test_has_payload_is_false_when_payload_is_empty()
                • test_has_payload_is_true_when_payload_exists()
                • test_string_representation_uses_display_text()
                • test_edges_with_same_values_are_equal()
                • test_edge_is_immutable()
                • test_payload_default_is_not_shared_between_instances()
                • test_edge_is_slot_based()
          📄 test_knowledge_graph_node.py
              ⚙️ Functions:
                • test_node_can_be_created_with_required_fields()
                • test_node_defaults_are_applied()
                • test_node_accepts_full_metadata()
                • test_display_name_returns_label()
                • test_display_text_returns_label()
                • test_display_description_returns_description()
                • test_has_payload_is_false_when_payload_is_empty()
                • test_has_payload_is_true_when_payload_exists()
                • test_string_representation_uses_display_text()
                • test_nodes_with_same_values_are_equal()
                • test_node_is_immutable()
                • test_payload_default_is_not_shared_between_instances()
                • test_node_is_slot_based()
          📄 test_knowledge_graph_resolver.py
              ⚙️ Functions:
                • test_resolver_can_be_created()
                • test_resolver_exposes_strategy()
                • test_resolver_delegates_analyze()
                • test_resolver_passes_same_context_to_strategy()
                • test_resolver_display_name()
                • test_resolver_display_text()
                • test_resolver_display_description()
                • test_resolver_string_representation()
              🏗️ Classes:
                • class StubKnowledgeGraphStrategy:
                  - __init__(self)
                  - analyze(self, context)
          📄 test_knowledge_graph_result.py
              ⚙️ Functions:
                • make_context()
                • make_graph()
                • make_non_empty_graph()
                • test_result_can_be_created()
                • test_result_defaults()
                • test_result_identifier_comes_from_context()
                • test_result_context_properties()
                • test_empty_result_has_no_graph()
                • test_result_can_contain_graph()
                • test_successful_result_with_graph_is_resolved()
                • test_successful_empty_result_is_unresolved()
                • test_failed_result_is_unresolved()
                • test_result_without_diagnostics()
                • test_result_with_diagnostics()
                • test_multiple_diagnostics_preserve_order()
                • test_result_confidence()
                • test_low_confidence_result()
                • test_confidence_boundary()
                • test_result_display_name()
                • test_successful_result_display_text()
                • test_failed_result_display_text()
                • test_diagnostic_has_display_priority()
                • test_graph_has_display_priority_when_no_diagnostics()
                • test_empty_result_has_empty_display_description()
                • test_result_is_slot_based()
                • test_result_is_immutable()
          📄 test_knowledge_graph_strategy.py
              ⚙️ Functions:
                • test_strategy_is_abstract()
                • test_strategy_display_name_uses_class_name()
                • test_strategy_display_text()
                • test_strategy_display_description()
                • test_strategy_string_representation()
                • test_strategy_analyze_contract()
        📂 lexical/
          📄 test_default_lexical_repository.py
              ⚙️ Functions:
                • make_repository()
                • test_get_entry_delegates()
                • test_find_entries_by_lemma_delegates()
                • test_find_entries_by_word_form_delegates()
                • test_find_senses_delegates()
                • test_search_delegates()
                • test_all_entries_delegates()
                • test_count_uses_canonical_repository_count()
                • test_display_contract()
          📄 test_default_lexical_resolution_strategy.py
              🏗️ Classes:
                • class TestDefaultLexicalResolutionStrategy:
                  - test_can_be_created(self)
                  - test_preserves_lookup_engine(self)
                  - test_resolve_delegates_to_lookup_engine(self)
                  - test_display_name(self)
                  - test_display_description(self)
                  - test_is_lexical_resolution_strategy(self)
          📄 test_default_lexical_service.py
              🏗️ Classes:
                • class TestDefaultLexicalService:
                  - test_is_lexical_service(self)
                  - test_preserves_repository(self)
                  - test_display_name(self)
                  - test_display_text(self)
                  - test_display_description(self)
                  - test_inherits_lookup_engine_behavior(self)
                  - test_can_resolve_using_inherited_service_logic(self)
                  - test_string_representation(self)
          📄 test_lexical_lookup_engine.py
              ⚙️ Functions:
                • make_context(subject)
                • make_entry(entry_id, headword)
                • test_engine_accepts_repository()
                • test_lookup_with_no_entries()
                • test_lookup_constructs_candidates()
                • test_lookup_detects_ambiguity()
                • test_custom_ranking_policy_is_used()
              🏗️ Classes:
                • class StudRankingPolicy:
                  - __init__(self)
                  - rank(self, candidates)
          📄 test_lexical_repository.py
              ⚙️ Functions:
                • test_lexical_repository_is_abstract()
                • test_concrete_repository_can_implement_contract()
                • test_repository_display_contract()
          📄 test_lexical_resolution_composition.py
              🏗️ Classes:
                • class TestLexicalResolutionComposition:
                  - test_canonical_repository_constructs_default_lexical_service(self)
                  - test_default_lexical_service_is_registered(self)
                  - test_registry_lexical_alias_returns_service(self)
                  - test_lexical_service_is_resolution_contributor(self)
                  - test_default_resolution_pipeline_accepts_lexical_service(self)
                  - test_lexical_service_is_first_pipeline_stage(self)
          📄 test_lexical_resolution_result.py
              ⚙️ Functions:
                • make_context()
                • make_candidate(score, sense)
                • test_empty_result()
                • test_result_with_candidate()
                • test_result_exposes_lexical_information()
                • test_result_detects_ambiguity()
                • test_low_confidence_is_not_confident()
                • test_display_text_for_resolved_result()
                • test_display_text_for_unresolved_result()
          📄 test_lexical_resolution_strategy.py
              ⚙️ Functions:
                • test_strategy_is_abstract()
          📄 test_lexical_resolver.py
              🏗️ Classes:
                • class TestLexicalResolver:
                  - test_can_be_created(self)
                  - test_preserves_strategy(self)
                  - test_resolve_delegates_to_strategy(self)
                  - test_display_name(self)
                  - test_display_description(self)
                  - test_string_representation(self)
          📄 test_lexical_service.py
              🏗️ Classes:
                • class TestLexicalService:
                  - _repository(self)
                  - _context(self)
                  - test_can_be_created(self)
                  - test_is_frozen(self)
                  - test_display_name(self)
                  - test_display_text(self)
                  - test_display_description(self)
                  - test_string_representation(self)
                  - test_lookup_engine_is_canonical_engine(self)
                  - test_lookup_engine_uses_same_repository(self)
                  - test_get_entry_delegates_to_repository(self)
                  - test_lookup_lemma_delegates_to_repository(self)
                  - test_lookup_word_form_delegates_to_repository(self)
                  - test_lookup_senses_delegates_to_repository(self)
                  - test_search_delegates_to_repository(self)
                  - test_all_entries_delegates_to_repository(self)
                  - test_count_delegates_to_repository(self)
                  - test_resolve_returns_lexical_resolution_result(self)
                  - test_resolve_uses_context_subject_as_word_form(self)
                  - test_contribute_enriches_resolution_result(self)
                  - test_contribute_preserves_context(self)
          📄 test_lookup_candidate.py
              ⚙️ Functions:
                • make_entry()
                • test_candidate_defaults()
                • test_candidate_properties()
                • test_candidate_with_sense()
                • test_candidate_is_immutable()
                • test_candidate_string_representation()
          📄 test_lookup_ranking_policy.py
              ⚙️ Functions:
                • candidate(headword, score, identifier)
                • test_default_policy_is_lookup_ranking_policy()
                • test_higher_score_is_ranked_first()
                • test_equal_scores_use_alphabetical_headword()
                • test_empty_candidates_return_empty_tuple()
                • test_generator_input_is_supported()
          📂 adapters/
            📄 test_monier_williams_adapter.py
                ⚙️ Functions:
                  • make_adapter()
                  • test_adapter_source()
                  • test_adapter_count()
                  • test_lookup_returns_exact_headword()
                  • test_lookup_normalizes_whitespace()
                  • test_lookup_unknown_headword_returns_empty()
                  • test_search_matches_headword()
                  • test_search_matches_definition()
                  • test_search_empty_query_returns_empty()
                  • test_all_records_returns_all_records()
                  • test_records_are_normalized()
                  • test_normalize_headword_requires_string()
            📄 test_monier_williams_mapper.py
                ⚙️ Functions:
                  • make_record()
                  • test_to_entry_preserves_source_information()
                  • test_to_sense_preserves_definition()
          📂 validators/
            📄 test_dictionary_entry_validator.py
                ⚙️ Functions:
                  • make_entry()
                  • test_valid_dictionary_entry_passes_validation()
                  • test_validator_supports_dictionary_entry()
                  • test_validator_rejects_arbitrary_object()
                  • test_empty_identifier_is_invalid()
                  • test_whitespace_identifier_is_invalid()
                  • test_empty_lemma_is_invalid()
                  • test_whitespace_lemma_is_invalid()
                  • test_empty_language_is_invalid()
                  • test_empty_source_produces_warning()
                  • test_source_is_not_required_for_structural_validity()
                  • test_empty_transliteration_is_allowed()
                  • test_empty_description_is_allowed()
                  • test_empty_senses_are_allowed()
                  • test_valid_sense_identifiers_are_accepted()
                  • test_multiple_invalid_required_fields_are_reported()
                  • test_invalid_object_returns_validation_result()
                  • test_invalid_object_produces_dic001()
                  • test_validator_can_be_reused()
                  • test_dictionary_entry_is_immutable()
                  • test_dictionary_entry_reports_senses()
                  • test_dictionary_entry_without_senses_reports_no_senses()
                  • test_validator_does_not_mutate_entry()
            📄 test_dictionary_sense_validator.py
                ⚙️ Functions:
                  • make_sense()
                  • test_valid_dictionary_sense_passes_validation()
                  • test_validator_supports_dictionary_sense()
                  • test_validator_rejects_arbitrary_object()
                  • test_empty_identifier_is_invalid()
                  • test_whitespace_identifier_is_invalid()
                  • test_empty_entry_id_is_invalid()
                  • test_whitespace_entry_id_is_invalid()
                  • test_empty_meaning_is_invalid()
                  • test_whitespace_meaning_is_invalid()
                  • test_empty_language_is_invalid()
                  • test_empty_source_produces_warning()
                  • test_empty_source_does_not_make_sense_invalid()
                  • test_empty_transliteration_is_allowed()
                  • test_empty_grammatical_label_is_allowed()
                  • test_empty_usage_is_allowed()
                  • test_empty_examples_are_allowed()
                  • test_valid_examples_are_accepted()
                  • test_multiple_required_fields_are_reported()
                  • test_invalid_object_returns_validation_result()
                  • test_invalid_object_produces_ds001()
                  • test_validator_can_be_reused()
                  • test_dictionary_sense_is_immutable()
                  • test_dictionary_sense_reports_examples()
                  • test_dictionary_sense_without_examples_reports_no_examples()
                  • test_dictionary_sense_reports_source()
                  • test_dictionary_sense_reports_grammatical_label()
                  • test_dictionary_sense_reports_transliteration()
                  • test_dictionary_sense_display_name_is_meaning()
                  • test_dictionary_sense_display_text_uses_transliteration()
                  • test_dictionary_sense_string_uses_display_text()
            📄 test_lexeme_validator.py
                ⚙️ Functions:
                  • make_lexeme()
                  • test_valid_lexeme_passes_validation()
                  • test_valid_lexeme_has_no_errors()
                  • test_validator_supports_lexeme()
                  • test_validator_does_not_support_arbitrary_object()
                  • test_empty_identifier_produces_lex001()
                  • test_whitespace_identifier_produces_lex001()
                  • test_identifier_issue_targets_identifier_field()
                  • test_empty_lemma_produces_lex002()
                  • test_whitespace_lemma_produces_lex002()
                  • test_lemma_issue_targets_lemma_field()
                  • test_empty_language_produces_lex003()
                  • test_empty_script_produces_lex004()
                  • test_default_language_and_script_are_valid()
                  • test_empty_transliteration_is_not_fatal()
                  • test_whitespace_transliteration_produces_warning()
                  • test_description_is_optional()
                  • test_empty_alias_set_is_valid()
                  • test_valid_aliases_are_accepted()
                  • test_multiple_invalid_required_fields_report_multiple_issues()
                  • test_validator_can_be_reused()
                  • test_validation_does_not_mutate_lexeme()
                  • test_invalid_object_returns_validation_result()
                  • test_invalid_object_produces_lex000()
            📄 test_lexical_composite_validator.py
                🏗️ Classes:
                  • class TestLexicalCompositeValidator:
                    - test_creates_default_validators(self)
                    - test_accepts_custom_validators(self)
                    - test_delegates_validation_to_composite(self)
                    - test_empty_composite_is_valid(self)
                    - test_validates_lexical_value_without_replacing_individual_rules(self)
                    - test_validators_are_returned_as_immutable_tuple(self)
            📄 test_lexical_relation_validator.py
                ⚙️ Functions:
                  • make_relation()
                  • issue_codes(result)
                  • test_supports_lexical_relation()
                  • test_does_not_support_unrelated_object()
                  • test_valid_relation_passes()
                  • test_empty_relation_id_is_invalid()
                  • test_blank_relation_id_is_invalid()
                  • test_empty_source_lexeme_id_is_invalid()
                  • test_blank_source_lexeme_id_is_invalid()
                  • test_empty_target_lexeme_id_is_invalid()
                  • test_blank_target_lexeme_id_is_invalid()
                  • test_self_relation_produces_warning()
                  • test_notes_are_optional()
                  • test_relation_type_is_preserved()
                  • test_relation_identity_is_stable()
                  • test_relation_to_dict_is_json_compatible()
                  • test_display_name_uses_relation_type()
                  • test_display_text_contains_relation()
                  • test_string_representation_uses_display_text()
                  • test_relation_is_immutable()
                  • test_relation_normalizes_text_fields()
            📄 test_lexical_source_validator.py
                ⚙️ Functions:
                  • make_source()
                  • issue_codes(result)
                  • test_supports_lexical_source()
                  • test_does_not_support_unrelated_object()
                  • test_valid_source_passes()
                  • test_empty_source_id_is_invalid()
                  • test_blank_source_id_is_invalid()
                  • test_empty_name_is_invalid()
                  • test_blank_name_is_invalid()
                  • test_source_type_is_preserved()
                  • test_language_is_required()
                  • test_script_is_required()
                  • test_version_is_optional()
                  • test_description_is_optional()
                  • test_https_url_is_valid()
                  • test_http_url_is_valid()
                  • test_non_http_url_produces_warning()
                  • test_display_name_uses_source_name()
                  • test_display_text_without_version()
                  • test_display_text_with_version()
                  • test_canonical_name_uses_dictionary_source()
                  • test_to_dict_serializes_source()
                  • test_source_is_immutable()
                  • test_source_normalizes_text_fields()
                  • test_has_version()
                  • test_has_description()
                  • test_has_url()
                  • test_string_representation_uses_display_text()
            📄 test_lexical_validator_registry.py
                🏗️ Classes:
                  • class TestLexicalValidatorRegistry:
                    - test_registry_can_be_created(self)
                    - test_custom_registry_starts_with_supplied_validators(self)
                    - test_register(self)
                    - test_register_replaces_existing_validator(self)
                    - test_register_rejects_none_model_type(self)
                    - test_register_rejects_none_validator(self)
                    - test_register_rejects_invalid_validator(self)
                    - test_get_returns_none_for_unknown_type(self)
                    - test_resolve_accepts_model_type(self)
                    - test_resolve_accepts_instance(self)
                    - test_resolve_uses_exact_type_before_base_type(self)
                    - test_resolve_falls_back_to_base_type(self)
                    - test_resolve_returns_none_when_unknown(self)
                    - test_unregister_existing_validator(self)
                    - test_unregister_unknown_validator(self)
                    - test_contains(self)
                    - test_clear(self)
                    - test_items(self)
                    - test_default_validator_classes_are_defined(self)
        📂 morphology/
          📄 test_default_morphological_repository.py
              🏗️ Classes:
                • class TestDefaultMorphologicalRepository:
                  - test_default_construction(self)
                  - test_rule_set_is_canonical(self)
                  - test_analyzer_is_canonical(self)
                  - test_analyzer_uses_repository_rule_set(self)
                  - test_count_matches_rule_set(self)
                  - test_nominal_categories(self)
                  - test_verbal_categories(self)
                  - test_all_categories(self)
                  - test_nominal_categories_are_not_empty(self)
                  - test_verbal_categories_are_not_empty(self)
                  - test_all_categories_are_not_empty(self)
                  - test_canonical_category_is_exposed(self, attribute)
                  - test_morphological_rule_set_alias(self)
                  - test_morphological_analyzer_alias(self)
          📄 test_default_morphological_resolution_kernel.py
              🏗️ Classes:
                • class TestDefaultMorphologicalResolutionKernel:
                  - test_can_be_created_with_repository(self)
                  - test_default_strategy_is_created(self)
                  - test_custom_strategy_is_preserved(self)
                  - test_resolution_strategy_returns_strategy(self)
                  - test_kernel_exposes_generic_resolution_kernel(self)
                  - test_resolve_delegates_to_strategy(self)
                  - test_call_delegates_to_resolve(self)
                  - test_display_contract(self)
                  - test_string_representation(self)
          📄 test_default_morphological_service.py
              🏗️ Classes:
                • class TestDefaultMorphologicalService:
                  - test_default_construction(self)
                  - test_default_repository_is_canonical_repository(self)
                  - test_repository_is_not_none(self)
                  - test_analyzer_is_canonical_analyzer(self)
                  - test_analyzer_comes_from_repository(self)
                  - test_rule_set_is_morphological_rule_set(self)
                  - test_rule_set_is_repository_rule_set(self)
                  - test_resolution_kernel_is_canonical_kernel(self)
                  - test_resolution_kernel_uses_service_repository(self)
                  - test_display_name(self)
                  - test_display_text_matches_display_name(self)
                  - test_string_representation(self)
                  - test_service_is_frozen(self)
                  - test_nominal_categories_are_exposed(self)
                  - test_verbal_categories_are_exposed(self)
                  - test_all_categories_are_exposed(self)
                  - test_vibhakti_is_exposed(self)
                  - test_vacana_is_exposed(self)
                  - test_linga_is_exposed(self)
                  - test_purusha_is_exposed(self)
                  - test_lakara_is_exposed(self)
                  - test_pada_is_exposed(self)
                  - test_prayoga_is_exposed(self)
                  - test_count_delegates_to_repository(self)
                  - test_repository_count_is_exposed_by_service(self)
                  - test_service_count_matches_rule_set_count(self)
          📄 test_grammatical_category_collection.py
              🏗️ Classes:
                • class TestGrammaticalCategoryCollection:
                  - _create_collection(self)
                  - test_default_construction(self)
                  - test_construction_with_items(self)
                  - test_iteration(self)
                  - test_len(self)
                  - test_indexing(self)
                  - test_first(self)
                  - test_last(self)
                  - test_first_on_empty_collection(self)
                  - test_last_on_empty_collection(self)
                  - test_contains_existing_category(self)
                  - test_find_existing_identifier(self)
                  - test_find_missing_identifier(self)
                  - test_collection_is_immutable(self)
                  - test_items_are_tuple(self)
                  - test_display_name(self)
                  - test_display_text(self)
                  - test_display_description(self)
                  - test_string_representation(self)
          📄 test_morphological_integration.py
              🏗️ Classes:
                • class TestMorphologicalIntegration:
                  - test_canonical_repository_exposes_morphology_service(self)
                  - test_morphology_service_uses_canonical_repository(self)
                  - test_morphology_service_uses_repository_analyzer(self)
                  - test_morphology_service_uses_repository_rule_set(self)
                  - test_morphology_service_uses_canonical_resolution_kernel(self)
                  - test_resolution_kernel_uses_same_repository(self)
                  - test_repository_count_is_consistent(self)
          📄 test_morphological_resolution_context.py
              🏗️ Classes:
                • class TestMorphologicalResolutionContext:
                  - _create_context(self)
                  - test_is_morphological_context(self)
                  - test_is_morphological_resolution_context(self)
                  - test_does_not_duplicate_state(self)
                  - test_display_name(self)
                  - test_display_text(self)
                  - test_display_description(self)
                  - test_string_representation(self)
                  - test_is_immutable(self)
        📂 pratyaya/
          📄 test_pratyaya_analysis_collection.py
              ⚙️ Functions:
                • make_analysis(identifier, pratyaya, confidence)
                • test_empty_collection_has_no_analyses()
                • test_non_empty_collection_has_analyses()
                • test_has_analyses_is_consistent_with_is_empty()
                • test_has_analyses_is_read_only_semantic_alias()
                • test_add_does_not_mutate_original_collection()
                • test_extend_combines_two_collections()
          📄 test_pratyaya_rule_set.py
              ⚙️ Functions:
                • make_context()
                • test_empty_rule_set_is_empty()
                • test_rule_set_stores_rules()
                • test_iteration_preserves_rule_order()
                • test_index_access_preserves_rule_order()
                • test_add_returns_new_rule_set()
                • test_add_preserves_existing_rule_order()
                • test_rule_set_is_immutable()
                • test_apply_returns_empty_tuple_for_empty_rule_set()
                • test_apply_invokes_matching_rules()
                • test_apply_skips_non_matching_rules()
                • test_apply_preserves_candidate_insertion_order()
                • test_apply_deduplicates_hashable_candidates()
                • test_apply_supports_unhashable_candidates()
                • test_apply_preserves_first_occurrence_of_unhashable_candidates()
                • test_apply_does_not_duplicate_identical_dictionary_candidates()
                • test_apply_returns_tuple()
                • test_apply_does_not_retain_previous_results()
              🏗️ Classes:
                • class FakeContext:
                • class FakePratyayaRule:
                  - __init__(self, identifier, candidates, applies)
                  - identifier(self)
                  - applies_to(self, context)
                  - apply(self, context)
        📂 reader/
          📄 __init__.py
          📄 test_chapter_view.py
              ⚙️ Functions:
                • make_position(chapter_id, sloka_id, word_id)
                • make_sloka(identifier, chapter_id, text)
                • make_chapter(slokas)
                • test_default_slokas_are_empty()
                • test_slokas_are_preserved_in_order()
                • test_index_access_returns_sloka()
                • test_sloka_returns_matching_sloka()
                • test_sloka_raises_for_unknown_identifier()
                • test_contains_chapter_position()
                • test_contains_matching_sloka_position()
                • test_contains_rejects_wrong_chapter_even_with_matching_sloka()
                • test_display_contract()
                • test_chapter_is_immutable()
          📄 test_default_reader_repository_navigation.py
              ⚙️ Functions:
                • _build_corpus()
                • repository()
                • test_document_property_returns_reader_document(repository)
                • test_get_document_without_id_returns_document(repository)
                • test_get_document_with_valid_id_returns_document(repository)
                • test_get_document_normalizes_identifier_to_string(repository)
                • test_get_document_unknown_id_raises_key_error(repository)
                • test_get_chapters_preserves_corpus_order(repository)
                • test_get_chapter_returns_expected_view(repository)
                • test_get_chapter_accepts_identifier_convertible_to_string(repository)
                • test_get_chapter_unknown_id_raises_key_error(repository)
                • test_get_chapter_slokas_returns_chapter_slokas(repository)
                • test_chapter_count_is_three(repository)
                • test_len_returns_chapter_count(repository)
                • test_next_chapter(repository)
                • test_previous_chapter(repository)
                • test_first_chapter_has_no_previous(repository)
                • test_last_chapter_has_no_next(repository)
                • test_chapter_navigation_preserves_projection_order(repository)
                • test_get_slokas_preserves_complete_corpus_order(repository)
                • test_get_sloka_returns_expected_view(repository)
                • test_get_sloka_unknown_id_raises_key_error(repository)
                • test_sloka_count_is_nine(repository)
                • test_next_sloka(repository)
                • test_previous_sloka(repository)
                • test_first_sloka_has_no_previous(repository)
                • test_last_sloka_has_no_next(repository)
                • test_sloka_navigation_crosses_chapter_boundary(repository)
                • test_sloka_previous_navigation_crosses_chapter_boundary(repository)
                • test_get_words_preserves_token_projection_order(repository)
                • test_get_word_returns_expected_view(repository)
                • test_get_word_unknown_id_raises_key_error(repository)
                • test_word_count_is_eighteen(repository)
                • test_get_sloka_words_returns_projected_words(repository)
                • test_get_sloka_words_unknown_sloka_raises_key_error(repository)
                • test_next_word(repository)
                • test_previous_word(repository)
                • test_first_word_has_no_previous(repository)
                • test_last_word_has_no_next(repository)
                • test_word_navigation_crosses_sloka_boundary(repository)
                • test_word_previous_navigation_crosses_sloka_boundary(repository)
                • test_unknown_chapter_raises_key_error(repository)
                • test_unknown_chapter_previous_raises_key_error(repository)
                • test_unknown_sloka_raises_key_error(repository)
                • test_unknown_sloka_previous_raises_key_error(repository)
                • test_unknown_word_raises_key_error(repository)
                • test_unknown_word_previous_raises_key_error(repository)
                • test_resolve_position_prefers_word_id(repository)
                • test_resolve_position_uses_sloka_when_word_id_absent(repository)
                • test_resolve_position_uses_chapter_when_only_chapter_id_exists(repository)
                • test_resolve_position_without_chapter_id_raises_value_error(repository)
                • test_document_position_points_to_first_chapter(repository)
                • test_projected_chapter_positions_are_canonical(repository)
                • test_projected_sloka_position_contains_parent_chapter(repository)
                • test_projected_word_position_contains_full_hierarchy(repository)
                • test_sloka_text_is_reconstructed_from_tokens(repository)
                • test_repository_statistics_are_consistent(repository)
                • test_empty_corpus_without_sections_is_rejected()
          📄 test_reader_controller.py
              ⚙️ Functions:
                • engine()
                • position()
                • next_position()
                • session(engine, position)
                • controller(session)
                • test_controller_stores_session(controller, session)
                • test_controller_exposes_engine(controller, engine)
                • test_controller_exposes_position(controller, position)
                • test_controller_exposes_session_state(controller, session)
                • test_open_creates_controller_from_session(monkeypatch, engine, position)
                • test_open_position_delegates(controller, session, next_position)
                • test_set_position_delegates(controller, session, next_position)
                • test_set_position_none_delegates(controller, session)
                • test_resolve_delegates(controller, session)
                • test_next_delegates(controller, session, next_position)
                • test_previous_delegates(controller, session, next_position)
                • test_back_delegates(controller, session, next_position)
                • test_forward_delegates(controller, session, next_position)
                • test_move_next_delegates(controller, session)
                • test_move_previous_delegates(controller, session)
                • test_clear_history_delegates(controller, session)
                • test_document_delegates_to_engine(controller, engine)
                • test_document_with_id_delegates_to_engine(controller, engine)
                • test_chapter_delegates_to_engine(controller, engine)
                • test_sloka_delegates_to_engine(controller, engine)
                • test_word_delegates_to_engine(controller, engine)
                • test_resolve_position_delegates_to_engine(controller, engine, position)
                • test_controller_display_properties(controller)
                • test_controller_string_representation(controller)
          📄 test_reader_controller_integration.py
              ⚙️ Functions:
                • _token(identifier, text, position)
                • _line(identifier, *tokens)
                • _paragraph(identifier, *lines)
                • _verse(identifier, *paragraphs)
                • _section(identifier, *verses)
                • _document(identifier, *sections)
                • corpus()
                • repository(corpus)
                • navigator(repository)
                • engine(repository, navigator)
                • controller(engine)
                • test_controller_opens_at_requested_position(controller)
                • test_controller_exposes_engine(controller, engine)
                • test_controller_resolves_document(controller)
                • test_controller_resolves_chapter(controller)
                • test_controller_resolves_sloka(controller)
                • test_controller_resolves_word(controller)
                • test_controller_resolves_current_position(controller)
                • test_controller_next_moves_to_next_word(controller)
                • test_controller_previous_moves_to_previous_word(controller)
                • test_controller_moves_across_sloka_boundary(controller)
                • test_controller_moves_across_chapter_boundary(controller)
                • test_controller_back_restores_previous_position(controller)
                • test_controller_forward_restores_forward_position(controller)
                • test_controller_clear_history_preserves_position(controller)
                • test_controller_set_position_establishes_new_root(controller)
                • test_controller_set_position_none_clears_position(controller)
                • test_controller_failed_navigation_preserves_position(controller)
                • test_controller_history_count_tracks_structural_navigation(controller)
                • test_controller_immutable_move_next_does_not_mutate_controller(controller)
                • test_controller_immutable_move_previous_does_not_mutate_controller(controller)
                • test_controller_display_state(controller)
          📄 test_reader_document.py
              ⚙️ Functions:
                • make_position(chapter_id, sloka_id, word_id)
                • make_chapter(identifier, title)
                • make_document(chapters)
                • test_default_chapters_are_empty()
                • test_chapters_are_preserved_in_order()
                • test_chapter_returns_matching_chapter()
                • test_chapter_raises_for_unknown_identifier()
                • test_contains_matches_chapter_position()
                • test_contains_accepts_deeper_position_in_existing_chapter()
                • test_display_contract()
                • test_reader_document_is_immutable()
                • test_reader_document_is_value_object()
          📄 test_reader_engine.py
              ⚙️ Functions:
                • repository()
                • navigator()
                • engine(repository, navigator)
                • chapter_position()
                • sloka_position()
                • word_position()
                • test_document_delegates_to_repository(engine, repository)
                • test_document_without_id_delegates_to_repository(engine, repository)
                • test_chapter_delegates_to_repository(engine, repository)
                • test_sloka_delegates_to_repository(engine, repository)
                • test_word_delegates_to_repository(engine, repository)
                • test_next_chapter_delegates_to_navigator(engine, navigator, chapter_position)
                • test_previous_chapter_delegates_to_navigator(engine, navigator, chapter_position)
                • test_next_sloka_delegates_to_navigator(engine, navigator, sloka_position)
                • test_previous_sloka_delegates_to_navigator(engine, navigator, sloka_position)
                • test_next_word_delegates_to_navigator(engine, navigator, word_position)
                • test_previous_word_delegates_to_navigator(engine, navigator, word_position)
                • test_resolve_delegates_to_repository_position_resolver(engine, repository, word_position)
                • test_move_next_uses_word_navigation_for_word_position(engine, navigator, word_position)
                • test_move_next_uses_sloka_navigation_for_sloka_position(engine, navigator, sloka_position)
                • test_move_next_uses_chapter_navigation_for_chapter_position(engine, navigator, chapter_position)
                • test_move_previous_uses_word_navigation_for_word_position(engine, navigator, word_position)
                • test_move_previous_uses_sloka_navigation_for_sloka_position(engine, navigator, sloka_position)
                • test_move_previous_uses_chapter_navigation_for_chapter_position(engine, navigator, chapter_position)
                • test_move_next_returns_none_at_boundary(engine, navigator, chapter_position)
                • test_move_previous_returns_none_at_boundary(engine, navigator, chapter_position)
          📄 test_reader_engine_integration.py
              ⚙️ Functions:
                • _token(identifier, text, position)
                • _line(identifier, *tokens)
                • _paragraph(identifier, *lines)
                • _verse(identifier, *paragraphs)
                • _section(identifier, *verses)
                • _document(identifier, *sections)
                • corpus()
                • repository(corpus)
                • navigator(repository)
                • engine(repository, navigator)
                • test_repository_projects_corpus_into_reader_document(repository)
                • test_repository_resolves_chapter_by_canonical_id(repository)
                • test_repository_resolves_sloka_by_canonical_id(repository)
                • test_repository_resolves_word_by_canonical_id(repository)
                • test_repository_resolves_chapter_position(repository)
                • test_repository_resolves_sloka_position(repository)
                • test_repository_resolves_word_position(repository)
                • test_navigator_moves_to_next_chapter(navigator)
                • test_navigator_moves_to_previous_chapter(navigator)
                • test_navigator_moves_to_next_sloka(navigator)
                • test_navigator_moves_to_previous_sloka(navigator)
                • test_navigator_moves_to_next_word(navigator)
                • test_navigator_moves_to_previous_word(navigator)
                • test_engine_resolves_chapter_through_repository(engine)
                • test_engine_resolves_sloka_through_repository(engine)
                • test_engine_resolves_word_through_repository(engine)
                • test_engine_moves_to_next_chapter(engine)
                • test_engine_moves_to_previous_chapter(engine)
                • test_engine_moves_to_next_sloka(engine)
                • test_engine_moves_to_next_word(engine)
                • test_engine_returns_none_after_last_chapter(engine)
                • test_engine_returns_none_before_first_chapter(engine)
                • test_engine_returns_none_after_last_word(engine)
                • test_reader_preserves_corpus_hierarchy_order(engine)
                • test_reader_preserves_sloka_order(engine)
                • test_reader_preserves_word_order(engine)
          📄 test_reader_interaction.py
              ⚙️ Functions:
                • make_position()
                • test_hover_creates_hover_context()
                • test_hover_preserves_position()
                • test_hover_exposes_hierarchy()
                • test_hover_exposes_canonical_id()
                • test_hover_is_immutable()
                • test_hover_does_not_change_position()
                • test_select_creates_selection_context()
                • test_select_preserves_position()
                • test_select_exposes_hierarchy()
                • test_select_exposes_level()
                • test_select_exposes_canonical_id()
                • test_select_can_be_converted_back_to_position()
                • test_selection_is_immutable()
                • test_hover_and_selection_are_distinct_contexts()
                • test_hover_does_not_create_selection()
          📄 test_reader_navigator.py
              ⚙️ Functions:
                • repository()
                • navigator(repository)
                • make_navigator()
                • test_next_chapter_uses_canonical_id()
                • test_previous_chapter_uses_canonical_id()
                • test_first_chapter_has_no_previous()
                • test_last_chapter_has_no_next()
                • test_next_chapter_rejects_missing_chapter_context()
                • test_previous_chapter_rejects_missing_chapter_context()
                • test_next_sloka_constructs_factory_position()
                • test_previous_sloka_constructs_factory_position()
                • test_first_sloka_has_no_previous()
                • test_last_sloka_has_no_next()
                • test_next_sloka_rejects_missing_sloka_context()
                • test_previous_sloka_rejects_missing_sloka_context()
                • test_next_word_preserves_structural_context()
                • test_previous_word_preserves_structural_context()
                • test_first_word_has_no_previous()
                • test_last_word_has_no_next()
                • test_next_word_rejects_missing_word_context()
                • test_previous_word_rejects_missing_word_context()
                • test_navigation_returns_new_immutable_position()
                • test_navigator_does_not_require_indices()
                • test_navigator_preserves_current_purana_id()
                • test_sloka_navigation_preserves_current_purana_id()
                • test_word_navigation_preserves_current_purana_id()
                • test_sloka_navigation_uses_view_structural_context()
                • test_word_navigation_uses_view_structural_context()
                • test_unknown_chapter_id_is_propagated()
                • test_unknown_sloka_id_is_propagated()
                • test_unknown_word_id_is_propagated()
                • test_navigator_accepts_injected_position_factory()
                • test_navigator_default_position_factory_is_available()
                • test_require_chapter_id_returns_string()
                • test_require_sloka_id_returns_string()
                • test_require_word_id_returns_string()
              🏗️ Classes:
                • class FakeView:
                • class FakeRepository:
                  - __init__(self)
                  - next_chapter(self, chapter_id)
                  - previous_chapter(self, chapter_id)
                  - next_sloka(self, sloka_id)
                  - previous_sloka(self, sloka_id)
                  - next_word(self, word_id)
                  - previous_word(self, word_id)
          📄 test_reader_position.py
              ⚙️ Functions:
                • test_purana_level_position()
                • test_chapter_level_position()
                • test_sloka_level_position()
                • test_word_level_position()
                • test_empty_purana_id_is_rejected()
                • test_missing_purana_id_is_rejected()
                • test_sloka_requires_chapter()
                • test_word_requires_sloka()
                • test_word_requires_complete_hierarchy()
                • test_level_is_purana()
                • test_level_is_chapter()
                • test_level_is_sloka()
                • test_level_is_word()
                • test_purana_level_predicates()
                • test_chapter_level_predicates()
                • test_sloka_level_predicates()
                • test_word_level_predicates()
                • test_canonical_id_at_purana_level()
                • test_canonical_id_at_chapter_level()
                • test_canonical_id_at_sloka_level()
                • test_canonical_id_at_word_level()
                • test_identifier_matches_canonical_id()
                • test_chapter_position_from_chapter_position()
                • test_chapter_position_from_sloka_position()
                • test_chapter_position_from_word_position()
                • test_chapter_position_requires_chapter()
                • test_sloka_position_from_sloka_position()
                • test_sloka_position_from_word_position()
                • test_sloka_position_requires_sloka()
                • test_word_position_from_word_position()
                • test_word_position_requires_word()
                • test_parent_position_is_a_new_immutable_reader_position()
                • test_to_dict_contains_canonical_fields()
                • test_to_dict_at_chapter_level()
                • test_string_representation_returns_canonical_id()
                • test_string_representation_at_chapter_level()
                • test_repr_contains_all_identifiers()
                • test_reader_position_is_immutable()
                • test_reader_position_cannot_change_purana_id()
                • test_equal_positions_are_equal()
                • test_different_positions_are_not_equal()
                • test_reader_position_is_hashable()
                • test_equal_positions_have_equal_hashes()
          📄 test_reader_position_factory.py
              ⚙️ Functions:
                • test_purana_constructs_reader_position()
                • test_purana_normalizes_identifier()
                • test_purana_rejects_none()
                • test_purana_rejects_empty_string()
                • test_purana_rejects_whitespace_only_identifier()
                • test_chapter_constructs_reader_position()
                • test_chapter_normalizes_identifiers()
                • test_chapter_rejects_none_purana_id()
                • test_chapter_rejects_none_chapter_id()
                • test_chapter_rejects_empty_identifiers()
                • test_chapter_rejects_whitespace_identifiers()
                • test_sloka_constructs_reader_position()
                • test_sloka_normalizes_identifiers()
                • test_sloka_rejects_none_purana_id()
                • test_sloka_rejects_none_chapter_id()
                • test_sloka_rejects_none_sloka_id()
                • test_sloka_rejects_empty_identifiers()
                • test_sloka_rejects_whitespace_identifiers()
                • test_word_constructs_reader_position()
                • test_word_normalizes_identifiers()
                • test_word_rejects_none_purana_id()
                • test_word_rejects_none_chapter_id()
                • test_word_rejects_none_sloka_id()
                • test_word_rejects_none_word_id()
                • test_word_rejects_empty_identifiers()
                • test_word_rejects_whitespace_identifiers()
                • test_factory_preserves_complete_hierarchy()
                • test_factory_positions_have_no_index_attributes()
                • test_factory_returns_immutable_positions()
                • test_factory_itself_is_immutable()
                • test_purana_factory_requires_keyword_argument()
                • test_chapter_factory_requires_keyword_arguments()
                • test_sloka_factory_requires_keyword_arguments()
                • test_word_factory_requires_keyword_arguments()
                • test_factory_converts_identifier_values_to_strings()
                • test_factory_produces_equal_positions_for_equal_identifiers()
                • test_factory_produces_distinct_positions_for_distinct_identifiers()
                • test_factory_position_serializes_correctly()
          📄 test_reader_result.py
              ⚙️ Functions:
                • position()
                • subject()
                • empty_result(position, subject)
                • test_reader_result_preserves_identifier(empty_result)
                • test_reader_result_preserves_position(empty_result, position)
                • test_reader_result_preserves_subject(empty_result, subject)
                • test_empty_result_has_no_lexical_result(empty_result)
                • test_empty_result_has_no_morphology_result(empty_result)
                • test_empty_result_has_no_sandhi_result(empty_result)
                • test_empty_result_has_no_samasa_result(empty_result)
                • test_empty_result_has_no_semantic_result(empty_result)
                • test_empty_result_has_no_pragmatics(empty_result)
                • test_empty_result_has_no_commentary(empty_result)
                • test_empty_result_has_zero_completed_stages(empty_result)
                • test_total_stage_count_is_seven(empty_result)
                • test_empty_result_completion_ratio_is_zero(empty_result)
                • test_empty_result_is_not_complete(empty_result)
                • test_lexical_result_counts_as_completed_stage(position, subject)
                • test_morphology_result_counts_as_completed_stage(position, subject)
                • test_sandhi_result_counts_as_completed_stage(position, subject)
                • test_samasa_result_counts_as_completed_stage(position, subject)
                • test_semantic_result_counts_as_completed_stage(position, subject)
                • test_pragmatics_counts_as_completed_stage(position, subject)
                • test_commentary_counts_as_completed_stage(position, subject)
                • test_all_resolution_stages_produce_complete_result(position, subject)
                • test_empty_result_has_no_cross_references(empty_result)
                • test_cross_references_are_counted(position, subject)
                • test_empty_result_has_no_canonical_sources(empty_result)
                • test_canonical_sources_are_counted(position, subject)
                • test_empty_result_has_no_metadata(empty_result)
                • test_metadata_is_available(position, subject)
                • test_missing_metadata_returns_default(empty_result)
                • test_display_name(empty_result)
                • test_display_text_uses_subject(empty_result, subject)
                • test_display_description(empty_result)
                • test_string_representation_uses_display_text(empty_result)
                • test_reader_result_is_immutable(empty_result)
                • test_reader_result_position_is_not_reassignable(empty_result)
                • test_reader_result_subject_is_not_reassignable(empty_result)
                • test_reader_result_has_expected_resolution_fields(empty_result)
                • test_reader_result_has_reference_fields(empty_result)
          📄 test_reader_selection_context.py
              ⚙️ Functions:
                • make_position(level)
                • test_reader_selection_context_from_position()
                • test_reader_selection_context_preserves_position(level)
                • test_reader_selection_context_exposes_identifiers(level)
                • test_reader_selection_context_delegates_state_to_position(level)
                • test_reader_selection_context_purana_hierarchy_flags()
                • test_reader_selection_context_chapter_hierarchy_flags()
                • test_reader_selection_context_sloka_hierarchy_flags()
                • test_reader_selection_context_word_hierarchy_flags()
                • test_reader_selection_context_display_contract()
                • test_reader_selection_context_is_immutable()
                • test_reader_selection_context_is_frozen()
                • test_reader_selection_context_requires_position()
                • test_reader_selection_context_accepts_direct_position_construction()
                • test_reader_selection_context_is_value_object_equal_by_value()
                • test_reader_selection_context_distinguishes_different_positions()
                • test_reader_selection_context_does_not_navigate()
                • test_reader_selection_context_does_not_manage_history()
                • test_reader_selection_context_level_is_canonical(level, expected_level)
          📄 test_reader_session.py
              ⚙️ Functions:
                • engine()
                • position()
                • next_position()
                • previous_position()
                • another_position()
                • make_session(engine, position)
                • test_session_constructs_with_engine(engine)
                • test_session_accepts_initial_position(engine, position)
                • test_history_defaults_to_new_history_instance(engine)
                • test_can_go_back_initially_false(engine)
                • test_can_go_forward_initially_false(engine)
                • test_open_establishes_position(engine, position)
                • test_open_establishes_initial_history_entry(engine, position)
                • test_open_clears_existing_history(engine, position, next_position)
                • test_set_position_establishes_new_root(engine, position, another_position)
                • test_set_position_none_clears_position_and_history(engine, position)
                • test_open_returns_supplied_position(engine, position)
                • test_next_returns_none_without_position(engine)
                • test_next_delegates_to_engine(engine, position, next_position)
                • test_next_updates_position(engine, position, next_position)
                • test_next_records_result_in_history(engine, position, next_position)
                • test_next_returns_none_at_boundary(engine, position)
                • test_next_does_not_change_state_when_engine_returns_none(engine, position, next_position)
                • test_next_can_record_multiple_structural_moves(engine, position, next_position, another_position)
                • test_previous_returns_none_without_position(engine)
                • test_previous_delegates_to_engine(engine, position, previous_position)
                • test_previous_updates_position(engine, position, previous_position)
                • test_previous_records_result_in_history(engine, position, previous_position)
                • test_previous_returns_none_at_boundary(engine, position)
                • test_previous_does_not_change_state_when_engine_returns_none(engine, position, next_position)
                • test_back_delegates_to_history_only(engine, position, next_position)
                • test_back_updates_position(engine, position, next_position)
                • test_back_returns_none_at_boundary(engine, position)
                • test_back_preserves_position_at_boundary(engine, position)
                • test_forward_delegates_to_history_only(engine, position, next_position)
                • test_forward_updates_position(engine, position, next_position)
                • test_forward_returns_none_at_boundary(engine, position)
                • test_next_after_back_creates_new_history_branch(engine, position, next_position, another_position)
                • test_previous_after_back_is_structural_not_history_navigation(engine, position, next_position, another_position)
                • test_clear_history_delegates_to_history(engine, position, next_position)
                • test_clear_history_does_not_clear_session_position(engine, position)
                • test_clear_history_disables_back_and_forward(engine, position, next_position)
                • test_display_name_without_position(engine)
                • test_display_name_with_position(engine, position)
                • test_display_text_without_position(engine)
                • test_display_text_with_position(engine, position)
                • test_display_description_without_position(engine)
                • test_display_description_with_position(engine, position)
                • test_string_representation_without_position(engine)
                • test_string_representation_with_position(engine, position)
                • test_next_then_back_restores_previous_position(engine, position, next_position)
                • test_next_then_back_then_forward_restores_next_position(engine, position, next_position)
                • test_failed_next_preserves_history_state(engine, position, next_position)
                • test_failed_previous_preserves_history_state(engine, position, next_position)
                • test_history_count_reflects_session_history(engine, position, next_position, another_position)
                • test_can_go_back_reflects_history(engine, position, next_position)
                • test_can_go_forward_reflects_history(engine, position, next_position)
          📄 test_reader_session_history.py
              ⚙️ Functions:
                • position_a()
                • position_b()
                • position_c()
                • position_d()
                • test_history_starts_empty()
                • test_first_record_becomes_current(position_a)
                • test_recording_new_positions_creates_back_history(position_a, position_b, position_c)
                • test_recording_same_position_does_not_create_duplicate(position_a)
                • test_back_moves_to_previous_position(position_a, position_b)
                • test_back_moves_through_multiple_positions(position_a, position_b, position_c)
                • test_back_returns_none_at_history_boundary(position_a)
                • test_back_on_empty_history_returns_none()
                • test_forward_restores_previous_position(position_a, position_b)
                • test_forward_moves_through_multiple_positions(position_a, position_b, position_c)
                • test_forward_returns_none_at_history_boundary(position_a, position_b)
                • test_forward_on_empty_history_returns_none()
                • test_back_and_forward_round_trip(position_a, position_b, position_c)
                • test_new_record_clears_forward_history(position_a, position_b, position_c, position_d)
                • test_previous_and_next_do_not_modify_history(position_a, position_b, position_c)
                • test_clear_removes_entire_history(position_a, position_b, position_c)
                • test_clear_forward_preserves_current_and_back_history(position_a, position_b, position_c)
                • test_record_rejects_invalid_position()
                • test_record_rejects_none()
                • test_history_does_not_mutate_reader_position(position_a)
                • test_display_name()
                • test_display_text_when_empty()
                • test_display_text_when_current_exists(position_a)
                • test_display_description(position_a, position_b, position_c)
                • test_string_representation_when_empty()
                • test_string_representation_with_current(position_a)
          📄 test_reader_session_history_integration.py
              ⚙️ Functions:
                • engine()
                • history()
                • position()
                • next_position()
                • previous_position()
                • session(engine, history)
                • test_session_starts_without_position(session)
                • test_session_uses_injected_history_instance(session, history)
                • test_set_position_establishes_initial_position(session, position)
                • test_set_position_records_initial_position_in_history(session, position)
                • test_set_position_creates_new_history_root(session, position, next_position)
                • test_session_next_delegates_to_reader_engine(session, engine, position, next_position)
                • test_session_next_records_result_in_history(session, engine, position, next_position)
                • test_session_next_returns_none_at_engine_boundary(session, engine, position)
                • test_session_previous_delegates_to_reader_engine(session, engine, position, previous_position)
                • test_session_previous_records_result_in_history(session, engine, position, previous_position)
                • test_session_previous_returns_none_at_engine_boundary(session, engine, position)
                • test_session_back_uses_history(session, position, next_position)
                • test_session_back_returns_none_at_history_root(session, position)
                • test_session_forward_uses_history(session, position, next_position)
                • test_session_forward_returns_none_without_forward_history(session, position)
                • test_session_history_round_trip(session, position, next_position, previous_position)
                • test_new_position_clears_forward_history(session, position, next_position, previous_position)
                • test_session_history_tracks_sloka_navigation(session, engine, position, next_position)
                • test_session_history_tracks_word_navigation(session, engine)
                • test_session_can_clear_history(session, position, next_position)
                • test_history_back_and_engine_navigation_remain_distinct(session, engine, position, next_position, previous_position)
                • test_history_state_reflects_current_session_position(session, engine, position, next_position)
          📄 test_reader_session_integration.py
              ⚙️ Functions:
                • _token(identifier, text, position)
                • _line(identifier, *tokens)
                • _paragraph(identifier, *lines)
                • _verse(identifier, *paragraphs)
                • _section(identifier, *verses)
                • _document(identifier, *sections)
                • corpus()
                • repository(corpus)
                • navigator(repository)
                • engine(repository, navigator)
                • test_session_opens_at_chapter(engine)
                • test_session_opens_at_sloka(engine)
                • test_session_opens_at_word(engine)
                • test_session_moves_to_next_chapter(engine)
                • test_session_moves_to_previous_chapter(engine)
                • test_session_moves_to_next_sloka(engine)
                • test_session_moves_to_previous_sloka(engine)
                • test_session_moves_to_next_word(engine)
                • test_session_moves_to_previous_word(engine)
                • test_session_returns_none_after_last_chapter(engine)
                • test_session_returns_none_before_first_chapter(engine)
                • test_navigation_does_not_mutate_original_session(engine)
                • test_session_result_preserves_chapter_sloka_hierarchy(engine)
                • test_session_resolve_reloads_current_position(engine)
          📄 test_reader_workspace.py
              ⚙️ Functions:
                • engine()
                • position()
                • session(engine, position)
                • controller(session)
                • workspace(controller)
                • test_workspace_stores_controller(workspace, controller)
                • test_workspace_exposes_session(workspace, session)
                • test_workspace_exposes_engine(workspace, engine)
                • test_workspace_exposes_position(workspace, position)
                • test_workspace_exposes_result_state(workspace)
                • test_workspace_exposes_navigation_state(workspace)
                • test_workspace_exposes_position_state(workspace)
                • test_workspace_derives_selection_from_current_position(workspace, position)
                • test_workspace_selection_is_derived_from_current_position(workspace, session)
                • test_workspace_selection_is_none_without_position(controller, session)
                • test_workspace_open_creates_controller(monkeypatch, engine, position)
                • test_workspace_display_contract(workspace, position)
                • test_workspace_string_representation(workspace)
                • test_workspace_does_not_duplicate_controller_state(workspace, session)
          📄 test_reader_workspace_integration.py
              ⚙️ Functions:
                • _token(identifier, text, position)
                • _line(identifier, *tokens)
                • _paragraph(identifier, *lines)
                • _verse(identifier, *paragraphs)
                • _section(identifier, *verses)
                • _document(identifier, *sections)
                • corpus()
                • repository(corpus)
                • navigator(repository)
                • engine(repository, navigator)
                • position()
                • workspace(engine, position)
                • test_workspace_open_integrates_with_reader_controller(workspace, engine, position)
                • test_workspace_exposes_active_reader_session(workspace, engine)
                • test_workspace_exposes_resolved_reader_state(workspace, position)
                • test_workspace_selection_tracks_session_position(workspace)
                • test_workspace_preserves_controller_navigation_semantics(workspace, position)
                • test_workspace_preserves_browser_history_semantics(workspace, position)
                • test_workspace_state_remains_controller_owned(workspace)
                • test_workspace_hover_does_not_change_position(workspace)
                • test_workspace_hover_does_not_change_history(workspace)
                • test_workspace_hover_is_transient(workspace)
                • test_workspace_select_produces_selection_context(workspace)
                • test_workspace_select_does_not_navigate(workspace)
                • test_workspace_select_does_not_change_history(workspace)
                • test_workspace_selection_reflects_current_position(workspace)
                • test_workspace_hover_then_select_preserves_same_position(workspace)
                • test_workspace_hover_select_then_controller_navigation(workspace)
                • test_workspace_navigation_updates_selection_after_interaction(workspace)
                • test_workspace_interaction_does_not_bypass_controller(workspace)
                • test_workspace_interaction_preserves_history_after_navigation(workspace)
          📄 test_sloka_view.py
              ⚙️ Functions:
                • make_position(chapter_id, sloka_id, word_id)
                • make_word(identifier, sloka_id, surface)
                • make_sloka(words, text)
                • test_default_words_are_empty()
                • test_words_are_preserved_in_order()
                • test_index_access_returns_word()
                • test_word_returns_matching_word()
                • test_word_raises_for_unknown_identifier()
                • test_contains_sloka_position()
                • test_contains_word_position()
                • test_contains_rejects_wrong_sloka()
                • test_display_prefers_sloka_text()
                • test_display_falls_back_to_title()
                • test_sloka_is_immutable()
          📄 test_word_view.py
              ⚙️ Functions:
                • make_position(word_id)
                • make_word(surface, transliteration, normalized)
                • test_default_fields_are_empty()
                • test_display_contract()
                • test_display_falls_back_to_reader_view()
                • test_transliteration_availability()
                • test_normalized_availability()
                • test_lexical_key_prefers_normalized_form()
                • test_lexical_key_falls_back_to_surface()
                • test_word_position_helpers_are_inherited()
                • test_word_is_immutable()
        📂 resolution/
          📄 test_default_resolution_pipeline.py
              ⚙️ Functions:
                • make_services()
                • test_default_pipeline_returns_resolution_pipeline()
                • test_default_pipeline_contains_five_stages()
                • test_default_pipeline_is_not_empty()
                • test_default_pipeline_contains_resolution_stages()
                • test_default_pipeline_stage_order()
                • test_lexical_service_is_first_contributor()
                • test_morphological_service_is_second_contributor()
                • test_sandhi_service_is_third_contributor()
                • test_samasa_service_is_fourth_contributor()
                • test_semantic_service_is_fifth_contributor()
                • test_default_pipeline_preserves_all_service_instances()
                • test_default_pipeline_executes_all_contributors()
                • test_default_pipeline_executes_contributors_in_order()
                • test_default_pipeline_uses_exact_registered_contributors()
                • test_default_pipeline_can_be_iterated()
                • test_default_pipeline_length_matches_stage_count()
              🏗️ Classes:
                • class RecordingContributor:
                  - __init__(self, label)
                  - contribute(self, aggregate, context)
          📄 test_lexical_resolution_stage.py
              ⚙️ Functions:
                • make_context(subject)
                • make_service()
                • make_contributor()
                • make_stage()
                • test_stage_can_be_constructed()
                • test_stage_is_resolution_stage()
                • test_stage_is_frozen()
                • test_stage_name()
                • test_stage_display_name()
                • test_stage_display_text()
                • test_stage_display_description()
                • test_stage_is_displayable()
                • test_stage_to_display_string()
                • test_execute_delegates_to_service()
                • test_execute_returns_exact_service_result()
                • test_execute_preserves_context()
                • test_contributor_is_preserved()
                • test_service_is_preserved()
                • test_stage_string_representation()
              🏗️ Classes:
                • class RecordingLexicalService:
                  - __init__(self)
                  - resolve(self, context)
                • class RecordingContributor:
                  - contribute(self, aggregate, context)
          📄 test_morphology_resolution_stage.py
              ⚙️ Functions:
                • make_context(subject)
                • make_service()
                • make_contributor()
                • make_stage()
                • test_stage_can_be_constructed()
                • test_stage_is_resolution_stage()
                • test_stage_is_frozen()
                • test_stage_name()
                • test_stage_display_name()
                • test_stage_display_text()
                • test_stage_display_description()
                • test_stage_is_displayable()
                • test_stage_to_display_string()
                • test_execute_delegates_to_service()
                • test_execute_returns_exact_service_result()
                • test_execute_preserves_context()
                • test_contributor_is_preserved()
                • test_service_is_preserved()
                • test_stage_string_representation()
              🏗️ Classes:
                • class RecordingMorphologicalService:
                  - __init__(self)
                  - resolve(self, context)
                • class RecordingContributor:
                  - contribute(self, aggregate, context)
          📄 test_resolution_context.py
              ⚙️ Functions:
                • make_context(**overrides)
                • test_context_can_be_created_with_required_fields()
                • test_context_defaults_are_empty()
                • test_context_preserves_optional_context()
                • test_display_properties()
                • test_subject_is_used_as_display_text()
                • test_source_language_and_script_flags()
                • test_empty_source_language_and_script_flags_are_false()
                • test_metadata_flag()
                • test_get_metadata_returns_value()
                • test_get_metadata_returns_default_for_missing_key()
                • test_get_metadata_returns_default_when_metadata_is_none()
                • test_context_is_immutable()
                • test_context_is_slot_based()
                • test_context_is_immutable_and_displayable()
                • test_string_representation_uses_display_text()
          📄 test_resolution_contributor.py
              ⚙️ Functions:
                • make_context(subject)
                • make_result(context)
                • test_resolution_contributor_is_abstract()
                • test_resolution_contributor_cannot_be_instantiated()
                • test_concrete_contributor_is_instance_of_contract()
                • test_contributor_has_no_instance_dict()
                • test_contributor_uses_empty_slots()
                • test_concrete_contributor_uses_empty_slots()
                • test_contributor_has_no_own_dict_descriptor()
                • test_concrete_contributor_has_no_own_dict_descriptor()
                • test_default_display_name_is_class_name()
                • test_display_text_delegates_to_display_name()
                • test_display_description_is_canonical()
                • test_contributor_is_displayable()
                • test_to_display_string_uses_display_text()
                • test_contribute_receives_aggregate_and_context()
                • test_contributor_preserves_aggregate_context()
                • test_contributor_accepts_equivalent_immutable_context()
                • test_contributor_rejects_different_context()
                • test_contributor_is_stateless()
                • test_contributor_does_not_mutate_aggregate()
                • test_string_representation_uses_display_text()
              🏗️ Classes:
                • class ConcreteResolutionContributor:
                  - contribute(self, aggregate, context)
          📄 test_resolution_diagnostic.py
              ⚙️ Functions:
                • make_diagnostic(**overrides)
                • test_diagnostic_can_be_created_with_required_fields()
                • test_default_values()
                • test_identifier_is_code()
                • test_display_name_is_code()
                • test_display_text_contains_uppercase_severity_and_message()
                • test_display_description_is_message()
                • test_information_severity()
                • test_warning_severity()
                • test_error_severity()
                • test_severity_checks_are_case_insensitive()
                • test_recoverable_error_is_not_fatal()
                • test_nonrecoverable_error_is_fatal()
                • test_non_error_is_never_fatal()
                • test_source_flag()
                • test_empty_source_flag()
                • test_diagnostic_is_immutable()
                • test_diagnostic_is_slot_based()
                • test_diagnostic_is_immutable_and_displayable()
                • test_string_representation_uses_display_text()
          📄 test_resolution_pipeline.py
              ⚙️ Functions:
                • make_context(subject)
                • make_stage(label, calls)
                • make_pipeline(labels)
                • test_pipeline_can_be_constructed()
                • test_pipeline_is_frozen()
                • test_pipeline_is_slot_based()
                • test_pipeline_stages_are_preserved()
                • test_display_name()
                • test_display_text()
                • test_display_description()
                • test_pipeline_is_displayable()
                • test_string_representation()
                • test_stage_count()
                • test_empty_pipeline()
                • test_non_empty_pipeline()
                • test_pipeline_is_iterable()
                • test_pipeline_len()
                • test_execute_returns_resolution_result()
                • test_execute_preserves_context()
                • test_execute_empty_pipeline_returns_initial_result()
                • test_execute_runs_stages_in_order()
                • test_execute_passes_context_to_every_stage()
                • test_execute_passes_same_aggregate_through_stages()
              🏗️ Classes:
                • class RecordingContributor:
                  - __init__(self, label, calls)
                  - contribute(self, aggregate, context)
          📄 test_resolution_result.py
              ⚙️ Functions:
                • make_context()
                • make_result(**overrides)
                • make_diagnostic()
                • test_result_can_be_created_with_context()
                • test_stage_results_default_to_none()
                • test_default_diagnostics_are_empty()
                • test_default_confidence_and_success()
                • test_display_properties()
                • test_stage_presence_flags_are_false_initially()
                • test_fully_resolved_is_false_initially()
                • test_diagnostic_properties()
                • test_with_lexical_returns_new_result()
                • test_with_morphology_preserves_existing_lexical_result()
                • test_with_sandhi_preserves_previous_results()
                • test_with_samasa_preserves_previous_results()
                • test_with_semantic_preserves_previous_results()
                • test_fully_resolved_requires_all_five_stages()
                • test_enrichment_preserves_context()
                • test_enrichment_preserves_diagnostics()
                • test_enrichment_preserves_confidence()
                • test_enrichment_preserves_success_state()
                • test_result_is_immutable()
                • test_result_is_slot_based()
                • test_result_is_immutable_and_displayable()
                • test_string_representation()
          📄 test_resolution_stage.py
              ⚙️ Functions:
                • make_context(subject)
                • make_result()
                • test_resolution_stage_can_be_constructed()
                • test_resolution_stage_stores_contributor()
                • test_resolution_stage_is_frozen()
                • test_resolution_stage_is_slot_based()
                • test_resolution_stage_display_name_delegates()
                • test_resolution_stage_display_text_delegates()
                • test_resolution_stage_display_description()
                • test_resolution_stage_context_type()
                • test_execute_delegates_to_contributor()
                • test_execute_passes_same_aggregate()
                • test_execute_passes_aggregate_context()
                • test_execute_returns_contributor_result()
                • test_string_representation_uses_display_text()
              🏗️ Classes:
                • class RecordingContributor:
                  - __init__(self)
                  - contribute(self, aggregate, context)
          📄 test_resolution_state.py
              ⚙️ Functions:
                • make_context()
                • make_state()
                • make_diagnostic()
                • test_state_can_be_created_with_context()
                • test_stage_results_default_to_none()
                • test_pipeline_metadata_defaults()
                • test_stage_flags_are_false_initially()
                • test_stage_count_is_zero_initially()
                • test_state_succeeds_initially()
                • test_state_is_slot_based()
                • test_state_is_mutable()
                • test_mark_completed_adds_stage()
                • test_mark_completed_preserves_stage_order()
                • test_mark_failed_records_failed_stage()
                • test_mark_completed_does_not_clear_failure()
                • test_add_diagnostic()
                • test_multiple_diagnostics_are_preserved()
                • test_set_metadata()
                • test_get_metadata_returns_value()
                • test_get_metadata_returns_default()
                • test_stage_result_flags_reflect_assigned_results()
                • test_state_can_accumulate_complete_pipeline_progress()
          📄 test_resolution_strategy.py
              ⚙️ Functions:
                • make_context(subject)
                • test_resolution_strategy_is_abstract()
                • test_resolution_strategy_cannot_be_instantiated()
                • test_concrete_strategy_is_instance_of_contract()
                • test_strategy_display_name_defaults_to_class_name()
                • test_strategy_display_text_delegates()
                • test_strategy_display_description_is_canonical()
                • test_strategy_is_displayable()
                • test_strategy_to_display_string()
                • test_resolve_returns_resolution_result()
                • test_resolve_preserves_context()
                • test_strategy_is_stateless()
                • test_string_representation_uses_display_text()
              🏗️ Classes:
                • class ConcreteResolutionStrategy:
                  - resolve(self, context)
          📄 test_resolver.py
              ⚙️ Functions:
                • make_context(subject)
                • test_resolver_can_be_constructed()
                • test_resolver_stores_strategy()
                • test_strategy_is_read_only()
                • test_resolver_display_name()
                • test_resolver_display_text()
                • test_resolver_display_description()
                • test_resolver_is_displayable()
                • test_resolver_to_display_string()
                • test_resolve_delegates_to_strategy()
                • test_resolve_passes_exact_context_to_strategy()
                • test_resolve_invokes_strategy_exactly_once()
                • test_resolve_returns_strategy_result()
                • test_resolver_string_representation()
              🏗️ Classes:
                • class RecordingStrategy:
                  - __init__(self)
                  - resolve(self, context)
                • class ConcreteResolver:
                  - display_name(self)
          📄 test_samasa_resolution_stage.py
              ⚙️ Functions:
                • make_context()
                • make_service()
                • make_contributor()
                • make_stage()
                • test_stage_can_be_constructed()
                • test_stage_is_resolution_stage()
                • test_stage_is_frozen()
                • test_stage_is_slot_based()
                • test_stage_name()
                • test_stage_display_name()
                • test_stage_display_text()
                • test_stage_display_description()
                • test_stage_is_displayable()
                • test_stage_to_display_string()
                • test_execute_delegates_to_service()
                • test_execute_returns_exact_service_result()
                • test_execute_preserves_context()
                • test_contributor_is_preserved()
                • test_service_is_preserved()
                • test_stage_string_representation()
              🏗️ Classes:
                • class RecordingSamasaService:
                  - __init__(self)
                  - resolve(self, context)
                • class RecordingContributor:
                  - contribute(self, aggregate, context)
          📄 test_sandhi_resolution_stage.py
              ⚙️ Functions:
                • make_context()
                • make_service()
                • make_contributor()
                • make_stage()
                • test_stage_can_be_constructed()
                • test_stage_is_resolution_stage()
                • test_stage_is_frozen()
                • test_stage_is_slot_based()
                • test_stage_name()
                • test_stage_display_name()
                • test_stage_display_text()
                • test_stage_display_description()
                • test_stage_is_displayable()
                • test_stage_to_display_string()
                • test_execute_delegates_to_service()
                • test_execute_returns_exact_service_result()
                • test_execute_preserves_context()
                • test_contributor_is_preserved()
                • test_service_is_preserved()
                • test_stage_string_representation()
              🏗️ Classes:
                • class RecordingSandhiService:
                  - __init__(self)
                  - resolve(self, context)
                • class RecordingContributor:
                  - contribute(self, aggregate, context)
          📄 test_semantic_resolution_stage.py
              ⚙️ Functions:
                • make_context()
                • make_service()
                • make_contributor()
                • make_stage()
                • test_stage_can_be_constructed()
                • test_stage_is_resolution_stage()
                • test_stage_is_frozen()
                • test_stage_is_slot_based()
                • test_stage_name()
                • test_stage_display_name()
                • test_stage_display_text()
                • test_stage_display_description()
                • test_stage_is_displayable()
                • test_stage_to_display_string()
                • test_execute_delegates_to_service()
                • test_execute_returns_exact_service_result()
                • test_execute_preserves_context()
                • test_contributor_is_preserved()
                • test_service_is_preserved()
                • test_stage_string_representation()
              🏗️ Classes:
                • class RecordingSemanticService:
                  - __init__(self)
                  - resolve(self, context)
                • class RecordingContributor:
                  - contribute(self, aggregate, context)
        📂 samasa/
          📄 test_default_samasa_resolution_kernel.py
              ⚙️ Functions:
                • make_context()
                • test_default_kernel_can_be_constructed()
                • test_default_kernel_exposes_generic_kernel()
                • test_default_kernel_builds_samasa_context()
              🏗️ Classes:
                • class StubSamasaRepository:
          📄 test_samasa_resolution_kernel.py
              ⚙️ Functions:
                • make_context()
                • test_kernel_delegates_to_strategy()
                • test_kernel_returns_canonical_resolution_result()
                • test_kernel_preserves_analysis_collection()
              🏗️ Classes:
                • class StubSamasaStrategy:
                  - __init__(self)
                  - analyze(self, context)
          📄 test_samasa_rule_set.py
              ⚙️ Functions:
                • make_context()
                • test_empty_rule_set()
                • test_rule_set_preserves_rule_order()
                • test_add_returns_new_rule_set()
                • test_add_does_not_mutate_original_rule_set()
                • test_apply_ignores_non_matching_rules()
                • test_apply_supports_unhashable_candidates()
                • test_apply_preserves_first_occurrence_of_unhashable_candidates()
                • test_apply_does_not_duplicate_identical_dictionary_candidates()
                • test_apply_preserves_candidate_insertion_order()
                • test_apply_returns_tuple()
                • test_apply_does_not_retain_previous_results()
                • test_display_name()
                • test_display_text()
                • test_display_description()
                • test_str_uses_display_text()
              🏗️ Classes:
                • class FakeSamasaRule:
                  - display_name(self)
                  - applies_to(self, context)
                  - apply(self, context)
          📄 test_samasa_service.py
              ⚙️ Functions:
                • make_context()
                • test_service_can_be_constructed()
                • test_service_creates_default_kernel()
                • test_service_resolve_returns_resolution_result()
              🏗️ Classes:
                • class StubSamasaRepository:
        📂 sandhi/
          📄 test_default_sandhi_repository.py
              ⚙️ Functions:
                • test_default_repository_can_be_constructed()
                • test_default_repository_implements_repository_contract()
                • test_default_repository_has_rule_set()
                • test_default_repository_is_empty_by_default()
                • test_default_repository_all_returns_rule_set()
                • test_default_repository_all_returns_repository_rule_set()
                • test_default_repository_count_is_zero_by_default()
                • test_default_repository_contains_missing_rule_returns_false()
                • test_default_repository_get_missing_rule_returns_none()
                • test_default_repository_search_returns_rule_set()
                • test_default_repository_search_is_empty_for_empty_repository()
                • test_default_repository_search_missing_query_returns_empty_set()
                • test_default_repository_display_name()
                • test_default_repository_display_text()
                • test_default_repository_display_description()
                • test_default_repository_has_dataclass_representation()
                • test_default_repository_instances_are_distinct()
                • test_default_repository_is_immutable()
                • test_default_repository_accepts_explicit_rule_set()
          📄 test_default_sandhi_resolution_kernel.py
              ⚙️ Functions:
                • make_repository()
                • make_context()
                • test_default_kernel_can_be_constructed()
                • test_default_kernel_uses_default_strategy()
                • test_default_kernel_accepts_custom_strategy()
                • test_default_kernel_is_immutable()
                • test_display_name()
                • test_display_text()
                • test_display_description()
                • test_string_representation()
                • test_resolution_strategy_returns_configured_strategy()
                • test_kernel_creates_generic_resolution_kernel()
                • test_kernel_is_recreated_on_each_access()
                • test_resolve_delegates_through_generic_kernel()
                • test_call_delegates_to_resolve()
              🏗️ Classes:
                • class StubSandhiRepository:
                • class StubSandhiStrategy:
                  - __init__(self, result)
                  - resolve(self, context)
          📄 test_default_sandhi_resolver.py
              ⚙️ Functions:
                • make_context()
                • test_default_resolver_can_be_constructed()
                • test_default_resolver_uses_default_strategy()
                • test_default_resolver_accepts_explicit_strategy()
                • test_default_resolver_display_name()
                • test_default_resolver_display_text()
                • test_default_resolver_display_description()
                • test_default_resolver_delegates_to_strategy()
                • test_default_resolver_returns_sandhi_result()
                • test_default_resolver_preserves_context()
                • test_default_resolver_string_representation()
              🏗️ Classes:
                • class StubSandhiStrategy:
                  - __init__(self, result)
                  - resolve(self, context)
          📄 test_default_sandhi_rule_set.py
              ⚙️ Functions:
                • test_default_rule_set_returns_sandhi_rule_set()
                • test_default_rule_set_contains_expected_number_of_rules()
                • test_default_rule_bundle_is_tuple()
                • test_default_rule_bundle_contains_expected_rule_types()
                • test_default_rule_order_is_preserved()
                • test_default_rule_set_contains_savarna_dirgha()
                • test_default_rule_set_contains_guna()
                • test_default_rule_set_contains_vrddhi()
                • test_default_rule_set_contains_jastva()
                • test_default_rule_set_contains_visarga_rules()
                • test_default_rule_set_contains_visarga_allophones()
                • test_default_rule_set_is_recreated_independently()
                • test_default_rule_bundle_is_not_empty()
                • test_default_rule_set_contains_only_sandhi_rules()
          📄 test_default_sandhi_service.py
              ⚙️ Functions:
                • test_default_service_can_be_constructed()
                • test_default_service_uses_default_repository()
                • test_default_service_accepts_explicit_repository()
                • test_default_service_display_name()
                • test_default_service_display_text()
                • test_default_service_display_description()
                • test_default_service_get_rule_delegates_to_repository()
                • test_default_service_get_missing_rule_returns_none()
                • test_default_service_search_rules_delegates_to_repository()
                • test_default_service_all_rules_delegates_to_repository()
                • test_default_service_rule_count_delegates_to_repository()
                • test_default_service_repository_is_read_only()
                • test_default_service_is_slot_based()
                • test_default_service_string_representation()
          📄 test_default_sandhi_strategy.py
              ⚙️ Functions:
                • make_context()
                • test_default_strategy_can_be_constructed()
                • test_default_strategy_uses_default_rule_set()
                • test_default_strategy_accepts_explicit_rule_set()
                • test_default_strategy_display_name()
                • test_default_strategy_display_text()
                • test_default_strategy_display_description()
                • test_default_strategy_resolve_returns_sandhi_result()
                • test_default_strategy_result_preserves_context()
                • test_default_strategy_result_preserves_identifier()
                • test_default_strategy_empty_rule_set_produces_failure()
                • test_default_strategy_empty_rule_set_produces_diagnostic()
                • test_default_strategy_empty_rule_set_is_unresolved()
                • test_default_strategy_uses_one_confidence_for_single_candidate()
                • test_default_strategy_multiple_candidates_use_lower_confidence()
                • test_default_strategy_success_has_no_diagnostics()
          📄 test_sandhi_repository.py
              ⚙️ Functions:
                • make_repository()
                • test_sandhi_repository_is_abstract()
                • test_sandhi_repository_cannot_be_instantiated()
                • test_concrete_repository_is_sandhi_repository()
                • test_repository_is_displayable()
                • test_repository_display_name_defaults_to_class_name()
                • test_repository_display_text_delegates_to_display_name()
                • test_repository_display_description_is_canonical()
                • test_repository_to_display_string_returns_display_text()
                • test_get_returns_rule_by_identifier()
                • test_get_returns_none_for_unknown_identifier()
                • test_contains_returns_true_for_existing_rule()
                • test_contains_returns_false_for_unknown_rule()
                • test_search_returns_matching_rule_set()
                • test_search_is_case_insensitive()
                • test_search_returns_empty_rule_set_when_no_match()
                • test_all_returns_complete_rule_set()
                • test_all_preserves_repository_order()
                • test_count_returns_total_rule_count()
                • test_empty_repository_contract()
              🏗️ Classes:
                • class ConcreteSandhiRule:
                  - __init__(self, identifier)
                  - identifier(self)
                  - applies_to(self, context)
                  - apply(self, context)
                • class InMemorySandhiRepository:
                  - __init__(self, rules)
                  - get(self, identifier)
                  - contains(self, identifier)
                  - search(self, query)
                  - all(self)
                  - count(self)
          📄 test_sandhi_resolution_kernel.py
              ⚙️ Functions:
                • make_context()
                • test_kernel_can_be_constructed_with_strategy()
                • test_kernel_uses_default_strategy_when_not_supplied()
                • test_kernel_is_immutable()
                • test_kernel_exposes_resolution_strategy()
                • test_display_name()
                • test_display_text()
                • test_display_description()
                • test_string_representation()
                • test_build_context_creates_sandhi_context()
                • test_build_context_preserves_resolution_fields()
                • test_resolve_adapts_context_before_strategy_delegation()
                • test_strategy_receives_sandhi_context_not_resolution_context()
                • test_call_delegates_to_resolve()
                • test_call_and_resolve_produce_same_strategy_result()
              🏗️ Classes:
                • class StubSandhiStrategy:
                  - __init__(self, result)
                  - resolve(self, context)
          📄 test_sandhi_resolver.py
              ⚙️ Functions:
                • make_context()
                • make_strategy()
                • make_resolver()
                • test_resolver_can_be_instantiated()
                • test_strategy_is_stored()
                • test_display_name()
                • test_display_text_matches_display_name()
                • test_display_description()
                • test_string_representation()
                • test_resolve_returns_sandhi_result()
                • test_resolve_delegates_to_strategy()
                • test_resolve_passes_context_to_strategy()
                • test_resolve_returns_strategy_result()
                • test_resolve_preserves_context()
                • test_resolve_can_be_called_multiple_times()
              🏗️ Classes:
                • class ConcreteSandhiStrategy:
                  - __init__(self)
                  - resolve(self, context)
          📄 test_sandhi_rule.py
              ⚙️ Functions:
                • make_context(subject)
                • test_sandhi_rule_is_abstract()
                • test_sandhi_rule_cannot_be_instantiated_directly()
                • test_concrete_rule_is_instance_of_sandhi_rule()
                • test_rule_display_name_defaults_to_class_name()
                • test_rule_display_text_delegates_to_display_name()
                • test_rule_display_description_is_canonical()
                • test_rule_is_displayable()
                • test_rule_to_display_string_returns_display_text()
                • test_rule_applies_to_matching_context()
                • test_rule_does_not_apply_to_non_matching_context()
                • test_rule_apply_returns_tuple_of_candidates()
                • test_rule_apply_returns_empty_tuple_when_not_applicable()
                • test_rule_string_representation_uses_display_text()
                • test_rule_is_stateless()
                • test_rule_preserves_context_contract()
              🏗️ Classes:
                • class ConcreteSandhiRule:
                  - applies_to(self, context)
                  - apply(self, context)
          📄 test_sandhi_rule_set.py
              ⚙️ Functions:
                • make_context()
                • test_default_rule_set_is_empty()
                • test_rule_set_is_immutable()
                • test_rule_set_is_slot_based()
                • test_rule_set_display_name()
                • test_rule_set_display_text_for_empty_set()
                • test_rule_set_display_description()
                • test_rule_set_string_representation()
                • test_add_returns_new_rule_set()
                • test_add_preserves_existing_rules()
                • test_add_does_not_mutate_original_rule_set()
                • test_apply_uses_matching_rules_only()
                • test_apply_collects_outputs_from_all_matching_rules()
                • test_apply_removes_duplicates_preserving_order()
                • test_apply_empty_rule_set_returns_empty_tuple()
                • test_len_returns_rule_count()
                • test_iteration_returns_rules_in_order()
                • test_indexing_returns_rule()
                • test_display_text_reflects_rule_count()
                • test_rule_set_is_displayable()
                • test_to_display_string_returns_display_text()
              🏗️ Classes:
                • class MatchingRule:
                  - applies_to(self, context)
                  - apply(self, context)
                • class NonMatchingRule:
                  - applies_to(self, context)
                  - apply(self, context)
                • class DuplicateOutputRule:
                  - applies_to(self, context)
                  - apply(self, context)
          📄 test_sandhi_service.py
              ⚙️ Functions:
                • make_repository()
                • make_service()
                • make_resolution_context()
                • test_service_can_be_constructed()
                • test_service_retains_repository()
                • test_service_is_immutable()
                • test_display_name()
                • test_display_text()
                • test_display_description()
                • test_string_representation()
                • test_resolution_kernel_is_created_with_repository()
                • test_resolution_kernel_is_recreated_from_repository()
                • test_resolve_delegates_to_resolution_kernel(monkeypatch)
                • test_contribute_returns_existing_aggregate_unchanged()
                • test_contribute_preserves_resolution_result()
                • test_service_is_resolution_contributor()
                • test_service_has_displayable_contract()
              🏗️ Classes:
                • class DummyRepository:
                  - get(self, identifier)
                  - contains(self, identifier)
                  - search(self, query)
                  - all(self)
                  - count(self)
          📄 test_sandhi_strategy.py
              ⚙️ Functions:
                • make_context()
                • test_strategy_is_abstract()
                • test_concrete_strategy_can_be_instantiated()
                • test_display_name_uses_class_name()
                • test_display_text_matches_display_name()
                • test_display_description_is_defined()
                • test_string_representation_uses_display_text()
                • test_resolve_returns_sandhi_result()
                • test_resolve_receives_context()
                • test_resolve_preserves_context()
                • test_resolve_preserves_subject()
                • test_resolve_produces_successful_result()
                • test_resolve_produces_expected_value()
              🏗️ Classes:
                • class ConcreteSandhiStrategy:
                  - __init__(self)
                  - resolve(self, context)
        📂 semantic/
          📄 test_default_semantic_resolution_kernel.py
              ⚙️ Functions:
                • make_context()
                • test_default_kernel_can_be_constructed()
                • test_default_kernel_exposes_generic_kernel()
                • test_default_kernel_builds_semantic_context()
                • test_default_kernel_preserves_metadata()
              🏗️ Classes:
                • class StubSemanticRepository:
          📄 test_semantic_relation_collection.py
              ⚙️ Functions:
                • make_relation(identifier, relation)
              🏗️ Classes:
                • class TestSemanticRelationCollection:
                  - test_can_be_created_empty(self)
                  - test_empty_collection_has_zero_count(self)
                  - test_empty_collection_is_empty(self)
                  - test_empty_collection_has_no_first_relation(self)
                  - test_accepts_relations_as_tuple(self)
                  - test_count_matches_number_of_relations(self)
                  - test_first_returns_first_relation(self)
                  - test_is_immutable_at_collection_level(self)
                  - test_add_returns_new_collection(self)
                  - test_extend_returns_new_collection(self)
                  - test_iteration(self)
                  - test_indexing(self)
                  - test_display_name(self)
                  - test_display_text(self)
                  - test_display_description(self)
                  - test_string_representation(self)
          📄 test_semantic_resolution_kernel.py
              ⚙️ Functions:
                • make_context()
                • test_kernel_delegates_to_strategy()
                • test_kernel_preserves_context()
                • test_kernel_returns_empty_analysis_collection_when_unresolved()
              🏗️ Classes:
                • class StubSemanticStrategy:
                  - __init__(self)
                  - analyze(self, context)
          📄 test_semantic_service.py
              ⚙️ Functions:
                • make_context()
                • test_service_can_be_constructed()
                • test_service_creates_default_kernel()
                • test_service_resolve_returns_resolution_result()
              🏗️ Classes:
                • class StubSemanticRepository:
      📂 importers/
        📄 run_all_tests.py
            🔹 Constants:
              • PROJECT_ROOT
              • TEST_MODULES
            ⚙️ Functions:
              • main()
      📂 integration/
        📄 test_import_error_recovery.py
            🔹 Constants:
              • PROJECT_ROOT
              • SAMPLE_FILE
            ⚙️ Functions:
              • main()
        📄 test_import_pipeline.py
            🔹 Constants:
              • PROJECT_ROOT
              • SAMPLE_FILE
            ⚙️ Functions:
              • main()
        📄 test_knowledge_service_registry.py
            ⚙️ Functions:
              • test_knowledge_service_registry_imports()
        📄 test_resolution_services.py
            ⚙️ Functions:
              • test_resolution_services_are_importable()
      📂 lexical/
        📄 __init__.py
        📄 demo.py
        📄 run_all_tests.py
            🔹 Constants:
              • PROJECT_ROOT
              • TEST_MODULES
            ⚙️ Functions:
              • main()
        📄 sample_lexemes.py
            ⚙️ Functions:
              • create_rama()
              • create_agni()
              • create_gam()
              • build_relation_demo()
        📄 test_dictionary_entry.py
            ⚙️ Functions:
              • test()
        📄 test_dictionary_sense.py
            ⚙️ Functions:
              • test()
        📄 test_integrity.py
            ⚙️ Functions:
              • test()
        📄 test_language.py
            ⚙️ Functions:
              • test()
        📄 test_lexeme.py
            ⚙️ Functions:
              • test()
        📄 test_relations.py
            ⚙️ Functions:
              • test()
        📄 test_script.py
            ⚙️ Functions:
              • test()
        📄 test_serialization.py
            ⚙️ Functions:
              • test()
        📂 models/
          📄 test_dictionary_entry.py
              ⚙️ Functions:
                • make_source()
                • make_metadata()
                • make_entry()
                • test_dictionary_entry_stores_identifier()
                • test_dictionary_entry_exposes_source()
                • test_dictionary_entry_exposes_source_name()
                • test_dictionary_entry_exposes_source_identifier()
                • test_dictionary_entry_exposes_dictionary_name()
                • test_dictionary_entry_exposes_dictionary_version()
                • test_dictionary_entry_exposes_entry_identifier()
                • test_dictionary_entry_exposes_headword()
                • test_dictionary_entry_exposes_transliteration()
                • test_dictionary_entry_exposes_volume()
                • test_dictionary_entry_exposes_page()
                • test_dictionary_entry_exposes_entry_number()
                • test_dictionary_entry_exposes_editor()
                • test_dictionary_entry_exposes_publisher()
                • test_dictionary_entry_exposes_publication_year()
                • test_dictionary_entry_exposes_primary_status()
                • test_dictionary_entry_exposes_citation()
                • test_dictionary_entry_exposes_display_title()
          📄 test_dictionary_entry_metadata.py
              ⚙️ Functions:
                • test_dictionary_entry_metadata_defaults()
                • test_dictionary_entry_metadata_stores_dictionary_information()
                • test_dictionary_entry_metadata_stores_headword()
                • test_dictionary_entry_metadata_display_title_prefers_headword()
                • test_dictionary_entry_metadata_display_title_falls_back_to_lemma()
                • test_dictionary_entry_metadata_display_title_falls_back_to_dictionary()
                • test_dictionary_entry_metadata_has_dictionary()
                • test_dictionary_entry_metadata_has_headword()
                • test_dictionary_entry_metadata_has_location()
                • test_dictionary_entry_metadata_has_no_location_by_default()
                • test_dictionary_entry_metadata_citation_dictionary_only()
                • test_dictionary_entry_metadata_citation_with_volume_and_page()
                • test_dictionary_entry_metadata_is_immutable()
          📄 test_dictionary_sense.py
              ⚙️ Functions:
                • make_metadata()
                • make_sense()
                • test_dictionary_sense_stores_identifier()
                • test_dictionary_sense_exposes_sense_number()
                • test_dictionary_sense_exposes_definition()
                • test_dictionary_sense_exposes_short_definition()
                • test_dictionary_sense_exposes_gloss()
                • test_dictionary_sense_exposes_semantic_domain()
                • test_dictionary_sense_exposes_usage_label()
                • test_dictionary_sense_exposes_register()
                • test_dictionary_sense_exposes_grammatical_note()
                • test_dictionary_sense_exposes_etymology()
                • test_dictionary_sense_exposes_examples()
                • test_dictionary_sense_exposes_citations()
                • test_dictionary_sense_exposes_cross_references()
                • test_dictionary_sense_is_a_leaf_node()
          📄 test_dictionary_sense_metadata.py
              ⚙️ Functions:
                • test_dictionary_sense_metadata_defaults()
                • test_dictionary_sense_metadata_stores_meaning()
                • test_dictionary_sense_metadata_stores_classification()
                • test_dictionary_sense_metadata_stores_linguistic_notes()
                • test_dictionary_sense_metadata_examples_default_to_empty_list()
                • test_dictionary_sense_metadata_citations_default_to_empty_list()
                • test_dictionary_sense_metadata_cross_references_default_to_empty_list()
                • test_dictionary_sense_metadata_stores_supporting_material()
                • test_dictionary_sense_metadata_stores_notes()
                • test_dictionary_sense_metadata_inherits_lemma()
          📄 test_lexeme.py
              ⚙️ Functions:
                • make_metadata()
                • make_lexeme()
                • test_lexeme_stores_identifier()
                • test_lexeme_exposes_lemma()
                • test_lexeme_exposes_transliteration()
                • test_lexeme_exposes_part_of_speech()
                • test_lexeme_exposes_root()
                • test_lexeme_exposes_frequency()
                • test_lexeme_exposes_language()
                • test_lexeme_exposes_script()
                • test_lexeme_exposes_status()
                • test_lexeme_metadata_is_preserved()
                • test_lexeme_uses_canonical_identifier()
                • test_lexeme_is_known_when_lemma_exists()
                • test_lexeme_metadata_display_title_defaults_to_lemma()
                • test_lexeme_metadata_can_have_explicit_title()
                • test_lexeme_metadata_has_title()
          📄 test_lexical_record.py
              ⚙️ Functions:
                • source()
                • metadata()
                • record(source, metadata)
                • test_lexical_record_is_constructed(record)
                • test_lexical_record_exposes_source(record, source)
                • test_lexical_record_exposes_source_name(record)
                • test_lexical_record_exposes_source_identifier(record)
                • test_lexical_record_preserves_metadata(record, metadata)
                • test_lexical_record_requires_source(metadata)
              🏗️ Classes:
                • class ConcreteLexicalRecord:
          📄 test_lexical_relation.py
              ⚙️ Functions:
                • make_metadata()
                • make_relation()
                • test_lexical_relation_stores_identifier()
                • test_lexical_relation_exposes_relation_type()
                • test_lexical_relation_exposes_source_identifier()
                • test_lexical_relation_exposes_target_identifier()
                • test_lexical_relation_exposes_directed()
                • test_lexical_relation_exposes_weight()
                • test_lexical_relation_exposes_confidence()
                • test_lexical_relation_exposes_source_dictionary()
                • test_lexical_relation_preserves_metadata()
                • test_lexical_relation_can_be_undirected()
                • test_lexical_relation_default_weight()
                • test_lexical_relation_default_confidence()
          📄 test_lexical_source.py
              ⚙️ Functions:
                • test_lexical_source_stores_identifier_and_name()
                • test_lexical_source_default_optional_fields()
                • test_lexical_source_preserves_full_source_information()
                • test_display_name_returns_name()
                • test_display_text_without_version()
                • test_display_text_with_version()
                • test_display_description_returns_description()
                • test_has_version()
                • test_has_publisher()
                • test_has_editor()
                • test_has_website()
                • test_lexical_source_is_immutable()
                • test_string_representation_without_version()
                • test_string_representation_with_version()
        📂 monier_williams/
          📄 test_parser.py
              ⚙️ Functions:
                • test_parser_reads_single_record()
                • test_parser_preserves_raw_text()
                • test_parser_handles_multiple_records()
        📂 registries/
          📄 test_lexical_registry.py
              ⚙️ Functions:
                • make_source()
                • make_lexeme(identifier)
                • make_dictionary_entry(identifier)
                • make_dictionary_sense(identifier)
                • make_lexical_relation(identifier)
                • test_registry_starts_empty()
                • test_add_registers_lexical_object()
                • test_register_many_registers_all_objects()
                • test_lookup_unknown_identifier_returns_none()
                • test_exists_reports_registered_identifier()
                • test_remove_removes_registered_object()
                • test_clear_removes_all_objects()
                • test_identifiers_returns_registered_identifiers()
                • test_items_returns_identifier_object_pairs()
                • test_iteration_returns_registered_objects()
                • test_lexemes_returns_only_lexemes()
                • test_dictionary_entries_returns_only_dictionary_entries()
                • test_dictionary_senses_returns_only_dictionary_senses()
                • test_lexical_relations_returns_only_lexical_relations()
                • test_typed_projections_are_empty_when_no_matching_objects_exist()
          📄 test_lexical_source_catalog.py
              ⚙️ Functions:
                • make_source(identifier, name)
                • test_empty_catalog_has_no_sources()
                • test_register_returns_source()
                • test_register_stores_source_by_identifier()
                • test_get_returns_none_for_unknown_source()
                • test_require_returns_registered_source()
                • test_require_unknown_source_raises_key_error()
                • test_exists_reports_registered_source()
                • test_contains_supports_identifier_membership()
                • test_register_many_registers_all_sources()
                • test_constructor_accepts_sources()
                • test_duplicate_identifier_is_rejected()
                • test_empty_identifier_is_rejected()
                • test_whitespace_identifier_is_rejected()
                • test_identifier_lookup_is_trimmed()
                • test_non_string_identifier_is_rejected()
                • test_non_lexical_source_is_rejected()
                • test_identifiers_preserve_registration_order()
                • test_sources_preserve_registration_order()
                • test_iteration_returns_registered_sources()
                • test_len_returns_source_count()
                • test_remove_returns_removed_source()
                • test_remove_unknown_source_raises_key_error()
                • test_clear_removes_all_sources()
        📂 repositories/
          📄 test_in_memory_lexical_repository.py
              ⚙️ Functions:
                • source()
                • repository(source)
                • lexeme()
                • entry()
                • sense()
                • test_repository_requires_lexical_source()
                • test_repository_exposes_source(repository, source)
                • test_repository_starts_empty(repository)
                • test_add_registers_lexeme(repository, lexeme)
                • test_add_registers_dictionary_entry(repository, entry)
                • test_add_registers_dictionary_sense(repository, sense)
                • test_add_rejects_unknown_object(repository)
                • test_add_many_registers_all_objects(repository, lexeme, entry, sense)
                • test_lookup_returns_none_for_unknown_identifier(repository)
                • test_identifier_is_normalized_to_string(repository, lexeme)
                • test_find_by_lemma_returns_matching_lexeme(repository, lexeme)
                • test_find_by_lemma_returns_matching_entry(repository, entry)
                • test_find_by_lemma_returns_both_matching_objects(repository, lexeme, entry)
                • test_find_by_lemma_returns_empty_tuple_when_missing(repository)
                • test_find_by_transliteration_returns_matching_objects(repository, lexeme, entry)
                • test_find_by_transliteration_returns_empty_tuple_when_missing(repository)
                • test_contains_checks_all_lexical_object_types(repository, lexeme, entry, sense)
                • test_general_search_finds_lexeme(repository, lexeme)
                • test_general_search_finds_entry(repository, entry)
                • test_general_search_finds_sense(repository, sense)
                • test_general_search_finds_by_identifier(repository, lexeme)
                • test_general_search_returns_empty_tuple_when_missing(repository)
                • test_counts_track_registered_objects(repository, lexeme, entry, sense)
                • test_readding_same_identifier_replaces_object(repository, lexeme)
                • test_clear_removes_all_objects(repository, lexeme, entry, sense)
          📄 test_lexical_repository.py
              ⚙️ Functions:
                • test_lexical_repository_is_abstract()
                • test_repository_cannot_be_instantiated_directly()
                • test_repository_exposes_source()
                • test_get_lexeme_contract()
                • test_get_entry_contract()
                • test_get_sense_contract()
                • test_find_by_lemma_contract()
                • test_find_by_transliteration_contract()
                • test_contains_contract()
                • test_search_contract()
                • test_repository_source_is_lexical_source()
                • test_repository_lookup_return_annotations_are_domain_objects()
                • test_repository_defines_all_required_operations()
              🏗️ Classes:
                • class StubLexicalRepository:
                  - __init__(self)
                  - source(self)
                  - get_lexeme(self, identifier)
                  - get_entry(self, identifier)
                  - get_sense(self, identifier)
                  - find_by_lemma(self, lemma)
                  - find_by_transliteration(self, transliteration)
                  - contains(self, identifier)
                  - search(self, query)
        📂 validators/
          📄 test_dictionary_entry_validator.py
              🔹 Constants:
                • _UNSET
              ⚙️ Functions:
                • make_source()
                • make_metadata()
                • make_dictionary_entry(identifier, source, metadata)
                • test_valid_dictionary_entry_passes_validation()
                • test_valid_dictionary_entry_has_no_errors()
                • test_empty_identifier_produces_lex001()
                • test_empty_identifier_issue_has_identifier_field()
                • test_empty_identifier_issue_has_message()
                • test_missing_source_produces_lex002()
                • test_missing_source_issue_has_source_field()
                • test_missing_source_issue_has_message()
                • test_missing_metadata_produces_lex003()
                • test_missing_metadata_issue_has_metadata_field()
                • test_missing_metadata_issue_has_message()
                • test_empty_identifier_and_missing_metadata_report_both()
                • test_empty_identifier_and_missing_source_report_both()
                • test_missing_source_and_metadata_report_both()
                • test_all_invalid_conditions_report_all_issues()
                • test_validator_can_be_reused()
                • test_validator_does_not_retain_previous_issues()
          📄 test_dictionary_sense_validator.py
              ⚙️ Functions:
                • make_metadata()
                • make_dictionary_sense()
                • test_valid_dictionary_sense_passes_validation()
                • test_valid_dictionary_sense_has_no_validation_errors()
                • test_valid_dictionary_sense_has_no_issues()
                • test_empty_identifier_produces_lex001()
                • test_empty_identifier_issue_has_identifier_field()
                • test_empty_identifier_issue_has_message()
                • test_whitespace_identifier_is_not_treated_as_empty()
                • test_missing_metadata_produces_lex002()
                • test_missing_metadata_issue_has_metadata_field()
                • test_missing_metadata_issue_has_message()
                • test_empty_identifier_and_missing_metadata_report_both_issues()
                • test_all_invalid_conditions_report_all_issues()
                • test_validator_accepts_sense_with_metadata_values()
                • test_metadata_object_itself_is_not_validated_for_empty_definition()
                • test_metadata_object_itself_is_not_validated_for_empty_gloss()
                • test_validator_can_be_reused()
                • test_validator_does_not_retain_previous_issues()
                • test_valid_result_contains_no_errors()
                • test_invalid_result_contains_errors()
          📄 test_lexical_relation_validator.py
              ⚙️ Functions:
                • make_metadata()
                • make_lexical_relation()
                • test_valid_lexical_relation_passes_validation()
                • test_valid_lexical_relation_has_no_validation_errors()
                • test_valid_lexical_relation_has_no_issues()
                • test_whitespace_identifier_is_not_treated_as_empty()
                • test_missing_identifier_produces_lex001()
                • test_missing_identifier_issue_has_identifier_field()
                • test_missing_identifier_issue_has_message()
                • test_missing_source_identifier_produces_lex002()
                • test_missing_source_identifier_issue_has_source_field()
                • test_missing_source_identifier_issue_has_message()
                • test_missing_target_identifier_produces_lex003()
                • test_missing_target_identifier_issue_has_target_field()
                • test_missing_target_identifier_issue_has_message()
                • test_missing_metadata_produces_lex004()
                • test_missing_metadata_issue_has_metadata_field()
                • test_missing_metadata_issue_has_message()
                • test_empty_identifier_and_missing_source_report_both()
                • test_empty_identifier_and_missing_target_report_both()
                • test_missing_source_and_target_report_both()
                • test_empty_identifier_and_missing_metadata_report_both()
                • test_all_invalid_conditions_report_all_issues()
                • test_missing_metadata_does_not_attempt_child_metadata_validation()
                • test_validator_accepts_relation_with_metadata_values()
                • test_validator_can_be_reused()
                • test_validator_does_not_retain_previous_issues()
                • test_valid_result_contains_no_errors()
          📄 test_lexical_source_validator.py
              ⚙️ Functions:
                • make_lexical_source()
                • test_valid_lexical_source_passes_validation()
                • test_valid_lexical_source_has_no_validation_errors()
                • test_valid_lexical_source_has_no_issues()
                • test_whitespace_identifier_is_not_treated_as_empty()
                • test_whitespace_name_is_not_treated_as_empty()
                • test_missing_identifier_produces_lex001()
                • test_missing_identifier_issue_has_identifier_field()
                • test_missing_identifier_issue_has_message()
                • test_missing_name_produces_lex002()
                • test_missing_name_issue_has_name_field()
                • test_missing_name_issue_has_message()
                • test_empty_identifier_and_missing_name_report_both()
                • test_all_invalid_conditions_report_all_issues()
                • test_optional_source_information_does_not_affect_validation()
                • test_empty_optional_source_information_is_valid()
                • test_display_name_returns_source_name()
                • test_display_text_without_version_returns_name()
                • test_display_text_with_version_includes_version()
                • test_display_description_returns_description()
                • test_has_version_is_false_when_version_is_empty()
                • test_has_version_is_true_when_version_is_present()
                • test_has_publisher_is_false_when_publisher_is_empty()
                • test_has_publisher_is_true_when_publisher_is_present()
                • test_has_editor_is_false_when_editor_is_empty()
                • test_has_editor_is_true_when_editor_is_present()
                • test_has_website_is_false_when_website_is_empty()
                • test_has_website_is_true_when_website_is_present()
                • test_validator_can_be_reused()
                • test_validator_does_not_retain_previous_issues()
                • test_valid_result_contains_no_errors()
      📂 panini/
        📄 test_conflict_pipeline.py
            🏗️ Classes:
              • class TestConflictPipeline:
                - test_pipeline_exists(self)
                - test_pipeline_returns_one_rule(self)
                - test_empty_conflict(self)
        📄 test_derivation_engine.py
            🏗️ Classes:
              • class TestDerivationEngine:
                - test_engine_creation(self)
                - test_empty_trace_on_creation(self)
                - test_context_creation(self)
                - test_engine_summary(self)
                - test_clear_trace(self)
        📄 test_execution_trace.py
            🏗️ Classes:
              • class TestExecutionTrace:
                - test_empty_trace(self)
                - test_append_step(self)
                - test_iteration(self)
        📄 test_vrddhir_adaic.py
            🏗️ Classes:
              • class TestVrddhirAdaic:
                - test_sutra_exists_in_catalog(self)
                - test_basic_derivation(self)
                - test_trace_contains_sutra(self)
                - test_pipeline_is_used(self)
                - test_engine_is_repeatable(self)
        📂 mocks/
          📄 mock_derivation_context.py
              ⚙️ Functions:
                • create_mock_context(text)
          📄 mock_rule.py
              🏗️ Classes:
                • class MockRule:
                  - __init__(self)
                  - supports(self, context)
                  - perform_transformation(self, context)
          📄 mock_subject.py
              🏗️ Classes:
                • class MockSubject:
                  - __post_init__(self)
                  - __str__(self)
        📂 testing/
          📄 panini_test_case.py
              🏗️ Classes:
                • class PaninianTestCase:
                  - create_context(self, text)
                  - create_rule(self)
                  - create_engine(self)
                  - assert_true(self, condition, message)
                  - assert_false(self, condition, message)
                  - assert_equal(self, actual, expected, message)
                  - assert_trace_length(self, trace, expected)
                  - assert_context_iteration(self, context, expected)
                  - assert_rule_applied(self, trace, sutra_number)
                  - print_trace(self, trace)
        📂 importers/
          📄 test_amarakosha_parser_import_result.py
              ⚙️ Functions:
                • parser()
                • minimal_valid_text()
                • test_parse_text_returns_canonical_import_result(parser, minimal_valid_text)
                • test_successful_parse_returns_completed_status(parser, minimal_valid_text)
                • test_successful_parse_has_no_errors(parser, minimal_valid_text)
                • test_successful_parse_reconciles_imported_object(parser, minimal_valid_text)
                • test_imported_object_is_not_lost_during_result_build(parser, minimal_valid_text)
                • test_statistics_are_reconciled_from_parser_context(parser, minimal_valid_text)
                • test_statistics_contain_expected_structural_counts(parser, minimal_valid_text)
                • test_unknown_line_produces_warning(parser, minimal_valid_text)
                • test_warning_does_not_make_import_unsuccessful(parser, minimal_valid_text)
                • test_structural_violation_is_recoverable(parser)
                • test_parser_converts_unexpected_exception_to_failed_result(parser, monkeypatch)
                • test_failed_result_contains_diagnostic(parser, monkeypatch)
                • test_parse_file_returns_canonical_import_result(parser, minimal_valid_text, tmp_path)
                • test_parse_file_rejects_unsupported_extension(parser, tmp_path)
                • test_parse_file_rejects_missing_file(parser, tmp_path)
                • test_amarakosha_parser_uses_canonical_status_vocabulary()
                • test_successful_result_is_terminal(parser, minimal_valid_text)
                • test_statistics_timing_is_started(parser, minimal_valid_text)
                • test_result_string_representation_is_available(parser, minimal_valid_text)
                • test_parser_context_remains_available_after_parse(parser, minimal_valid_text)
    📂 tools/
      📄 diagnose_semantic_rules.py
    📂 utils/
      📄 __init__.py
      📄 helpers.py
          ⚙️ Functions:
            • compact_none(data)
      📄 logger.py
          ⚙️ Functions:
            • get_logger(name)
