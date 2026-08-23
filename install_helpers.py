import os
import sys
import shutil


PIVY_HEADER = """\
#ifdef __PIVY__
%%include %s
#endif

"""


def write_if_changed(path, contents):
    """Write text only when the destination content differs."""

    try:
        with open(path, "r") as existing_file:
            if existing_file.read() == contents:
                return False
    except FileNotFoundError:
        pass

    with open(path, "w") as output_file:
        output_file.write(contents)
    return True


def swigified_header_contents(contents, include_file):
    swig_header = PIVY_HEADER % include_file
    if swig_header in contents:
        return contents

    lines = contents.splitlines(True)
    for line_number, line in enumerate(lines):
        if line.find("#include ") != -1:
            ins_line_nr = line_number
            break
    else:
        return None

    lines.insert(ins_line_nr, swig_header)
    return "".join(lines)


def swigify_header(header_file, include_file):
    with open(header_file, "r") as header:
        contents = header.read()

    swigified = swigified_header_contents(contents, include_file)
    if swigified is None:
        print("[failed]")
        sys.exit(1)
    if swigified == contents:
        return False

    write_if_changed(header_file, swigified)
    sys.stdout.write("create swigified header: " + header_file + "\n")
    return True


def copy_and_swigify_header(interface_dir, include_dir, fname):
    """Copy the header file to the local include directory. Add an
    #include line at the beginning for the SWIG interface file..."""

    if fname.endswith(".i"):  # consider ".i" files
        fname_h = fname[:-2] + ".h"  # corresponding ".h" file
        from_file = os.path.join(include_dir, fname_h)
        to_file = os.path.join(interface_dir, fname_h)

    elif fname.endswith(".fix"):  # just drop the suffix
        # fixes for SWIG 1.3.21 and upwards
        # (mostly workarounding swig's preprocessor "function like macros"
        # preprocessor bug when no parameters are provided which then results
        # in no constructors being created in the wrapper)
        fname_nosuffix = fname[:-4]
        from_file = os.path.join(interface_dir, fname)
        to_file = os.path.join(interface_dir, fname_nosuffix)

    elif sys.platform == "win32" and fname.endswith(".win32"):  # just drop the suffix
        # had to introduce this because windows is a piece of crap
        fname_nosuffix = fname[:-6]
        from_file = os.path.join(interface_dir, fname)
        to_file = os.path.join(interface_dir, fname_nosuffix)

    else:  # ignore other extensions
        return

    if not os.path.isfile(os.path.join(from_file)):
        return

    # Copy only when the source content differs.  CMake runs this helper on
    # every configure, and needless mtime changes force the large SWIG
    # wrappers to rebuild.
    if fname.endswith(".i"):  # consider ".i" files
        with open(from_file, "r") as source_file:
            source_contents = source_file.read()
        swigified = swigified_header_contents(source_contents, fname)
        if swigified is None:
            print("[failed]")
            sys.exit(1)
        if write_if_changed(to_file, swigified):
            sys.stdout.write("create swigified header: " + to_file + "\n")
    else:
        with open(from_file, "rb") as source_file:
            source_contents = source_file.read()
        try:
            with open(to_file, "rb") as destination_file:
                destination_contents = destination_file.read()
        except FileNotFoundError:
            destination_contents = None
        if destination_contents != source_contents:
            with open(to_file, "wb") as destination_file:
                destination_file.write(source_contents)


def swigify(interface_dir, include_dir, component="Inventor"):
    """Prepare header files for SWIG"""

    # find files within interface_dir/component
    interface_walker = os.walk(os.path.join(interface_dir, component))
    for dirpath, _, fnames in interface_walker:
        for fname in fnames:
            # only the filename relative to below interface_dir is needed
            relative_fname = os.path.join(dirpath[1+len(interface_dir):], fname)
            copy_and_swigify_header(interface_dir, include_dir, relative_fname)


if __name__ == "__main__":
    swigify(sys.argv[1], sys.argv[2])
