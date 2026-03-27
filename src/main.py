from markdown_blocks import markdown_to_html_node, extract_title
import shutil
import os

from textnode import TextNode, TextType

def main():
   if os.path .exists("public"):
      shutil.rmtree("public")
   os.mkdir("public")

   dummy_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
   print(dummy_node)
   recursive_function("static", "public")

   # generate_page("content/index.md", "template.html", "public/index.html")

   # generate_page("content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/index.html")
   # generate_page("content/blog/tom/index.md", "template.html", "public/blog/tom/index.html")
   # generate_page("content/blog/majesty/index.md", "template.html", "public/blog/majesty/index.html")
   # generate_page("content/contact/index.md", "template.html", "public/contact/index.html")
   generate_pages_recursive("content", "template.html", "public")

def recursive_function(source, destination):
   if os.path.exists(destination):
      shutil.rmtree(destination)
      os.mkdir(destination)
      for s in os.listdir(source):
         joined = os.path.join(source, s)
         if os.path.isfile(joined):
            shutil.copy(joined, destination)
            print(joined)
         else:
            new_des = os.path.join(destination, s)
            os.mkdir(new_des)
            recursive_function(joined, new_des)

def generate_page(from_path, template_path, dest_path):
   print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

   with open(from_path, "r") as f:
      markdown_content = f.read()
   with open(template_path, "r") as f:
      template = f.read()
   
   html_node = markdown_to_html_node(markdown_content)
   content_html = html_node.to_html()

   title = extract_title(markdown_content)

   full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)

   os.makedirs(os.path.dirname(dest_path), exist_ok=True)
   with open(dest_path, "w") as f:
      f.write(full_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Generating pages from {dir_path_content} to {dest_dir_path} using {template_path}")
    
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)

        if os.path.isfile(from_path):
            if filename.endswith(".md"):
                dest_html_path = dest_path.replace(".md", ".html")
                generate_page(from_path, template_path, dest_html_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)



main()
