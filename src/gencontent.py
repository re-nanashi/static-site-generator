import os

from markdown_blocks import (
    BlockType, markdown_to_html_node, markdown_to_blocks, block_to_block_type)


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == BlockType.block_type_heading:
            if block[:7].count("#") == 1:
                return block[2:]
    raise ValueError(
        "Error encountered while extracting title. No title found.")


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page from {from_path} to {dest_path} using {template_path}.")
    if not os.path.exists(from_path):
        # Raise an exception if no such file exists
        raise Exception(
            f"File does not exist: {from_path}. Exiting program...")

    md_file = open(from_path, "r")
    md_content = md_file.read()
    md_file.close()

    template_file = open(template_path, "r")
    html_template = template_file.read()
    template_file.close()

    # Convert the markdown to html code
    html_title = extract_title(md_content)
    html_to_inject = markdown_to_html_node(md_content).to_html()
    # Inject the converted markdown to the html template
    html_template = html_template.replace("{{ Title }}", str(html_title))
    html_template = html_template.replace("{{ Content }}", html_to_inject)

    # Write the new HTML to a file at dest_path.
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    output_file = open(dest_path, "w")
    output_file.write(html_template)
    output_file.close()


def generate_pages_r(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    for filename in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, filename)
        if os.path.isfile(src_path) and filename[-3:] == ".md":
            dest_path = os.path.join(
                dest_dir_path, f"{filename.split('.')[0]}.html")
            try:
                # TODO: Create new file with +1 number to the filename if filename already exists
                generate_page(src_path, template_path, dest_path)
            except:
                raise Exception("Error occured while generating file.")
        else:
            dest_path = os.path.join(dest_dir_path, filename)
            generate_pages_r(src_path, template_path, dest_path)
