# Generate Website

Source code for the transforming my website from Markdown files to HTML files and automatically
generate a `sitemap.txt` file.

The tool is configured through a `config.yaml`-file with the following configuration:

```yaml
url_prefix: <url prefix used when generating the sitemap>
root_dir: <directory where files can be found>
website_destination_folder: <destination folder for compiled files>
template: <Pandoc template file>

files_to_process:
- glob: <pattern used to find files, relative to root_dir>
  type: <one of text|code-base|copy>
```

For more information, visit the main website at [https://www.turtlestoffel.com][1].
In case of questions or comments, feel free to reach out in the [Discord][2].

[1]: https://www.turtlestoffel.com
[2]: https://discord.gg/UFECxB85ed
