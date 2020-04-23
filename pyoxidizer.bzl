def make_dist():
    return default_python_distribution()

def make_exe(dist):
    python_config = PythonInterpreterConfig(
        run_module="gork.main",
        #     bytes_warning=0,
        #     dont_write_bytecode=True,
        #     ignore_environment=True,
        #     inspect=False,
        #     interactive=False,
        #     isolated=False,
        #     legacy_windows_fs_encoding=False,
        #     legacy_windows_stdio=False,
        #     no_site=True,
        #     no_user_site_directory=True,
        #     optimize_level=0,
        #     parser_debug=False,
        #     stdio_encoding=None,
        #     unbuffered_stdio=False,
        #     filesystem_importer=False,
        #     sys_frozen=False,
        #     sys_meipass=False,
        #     sys_paths=None,
        #     raw_allocator=None,
        #     terminfo_resolution="dynamic",
        #     terminfo_dirs=None,
        #     use_hash_seed=False,
        #     verbose=0,
        #     write_modules_directory_env=None,
    )

    exe = dist.to_python_executable(
        name="gork",
        config=python_config,
        extension_module_filter="all",
        resources_policy="prefer-in-memory-fallback-filesystem-relative:lib",
        include_sources=False,
        include_resources=False,
        include_test=False,
    )

    exe.add_in_memory_python_resources(dist.pip_install(["-r", "requirements.txt"]))
    exe.add_in_memory_python_resources(dist.read_package_root(
       path=".",
       packages=["gork"],
    ))

    # Filter all resources collected so far through a filter of names
    # in a file.
    #exe.filter_from_files(files=["/path/to/filter-file"]))

    return exe

def make_embedded_resources(exe):
    return exe.to_embedded_resources()

def make_install(exe):
    # Create an object that represents our installed application file layout.
    files = FileManifest()

    # Add the generated executable to our install layout in the root directory.
    files.add_python_resource(".", exe)

    return files

# Tell PyOxidizer about the build targets defined above.
register_target("dist", make_dist)
register_target("exe", make_exe, depends=["dist"], default=True)
register_target("resources", make_embedded_resources, depends=["exe"], default_build_script=True)
register_target("install", make_install, depends=["exe"])

# Resolve whatever targets the invoker of this configuration file is requesting
# be resolved.
resolve_targets()

# END OF COMMON USER-ADJUSTED SETTINGS.
#
# Everything below this is typically managed by PyOxidizer and doesn't need
# to be updated by people.

PYOXIDIZER_VERSION = "0.7.0"
PYOXIDIZER_COMMIT = "UNKNOWN"
