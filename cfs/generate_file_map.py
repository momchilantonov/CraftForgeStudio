import os
import sys
import requests
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class FileInfo:
    """Data class representing a file in the repository"""
    path: str
    raw_url: str
    size: int
    type: str = "blob"

    @property
    def filename(self) -> str:
        """Extract filename from path"""
        return Path(self.path).name

    @property
    def directory(self) -> str:
        """Extract directory path from full path"""
        parent = Path(self.path).parent
        return str(parent) if str(parent) != "." else "root"

    @property
    def extension(self) -> str:
        """Get file extension"""
        return Path(self.path).suffix


class GitHubAPIClient:
    """Client for interacting with GitHub API"""

    BASE_API_URL = "https://api.github.com"
    BASE_RAW_URL = "https://raw.githubusercontent.com"

    def __init__(self, token: Optional[str] = None):
        """
        Initialize GitHub API client

        Args:
            token: Optional GitHub personal access token for authentication
        """
        self.token = token
        self.session = requests.Session()

        if token:
            self.session.headers.update({
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json"
            })

    def get_repository_info(self, owner: str, repo: str) -> Dict:
        """
        Fetch repository information

        Args:
            owner: GitHub username or organization
            repo: Repository name

        Returns:
            Dictionary with repository information
        """
        url = f"{self.BASE_API_URL}/repos/{owner}/{repo}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_default_branch(self, owner: str, repo: str) -> str:
        """
        Get the default branch name for a repository

        Args:
            owner: GitHub username or organization
            repo: Repository name

        Returns:
            Default branch name (e.g., 'main' or 'master')
        """
        repo_info = self.get_repository_info(owner, repo)
        return repo_info.get("default_branch", "main")

    def get_repository_tree(self, owner: str, repo: str, branch: str) -> Dict:
        """
        Fetch complete repository tree recursively

        Args:
            owner: GitHub username or organization
            repo: Repository name
            branch: Branch name

        Returns:
            Dictionary containing complete tree structure
        """
        url = f"{self.BASE_API_URL}/repos/{owner}/{repo}/git/trees/{branch}"
        params = {"recursive": "1"}

        response = self.session.get(url, params=params)
        response.raise_for_status()

        return response.json()

    def check_rate_limit(self) -> Dict:
        """
        Check current API rate limit status

        Returns:
            Dictionary with rate limit information
        """
        url = f"{self.BASE_API_URL}/rate_limit"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()


class RepositoryAnalyzer:
    """Analyzes repository structure and generates file information"""

    def __init__(self, api_client: GitHubAPIClient):
        """
        Initialize repository analyzer

        Args:
            api_client: GitHubAPIClient instance
        """
        self.api_client = api_client

    def analyze(self, owner: str, repo: str, branch: Optional[str] = None) -> List[FileInfo]:
        """
        Analyze repository and extract file information

        Args:
            owner: GitHub username or organization
            repo: Repository name
            branch: Branch name (auto-detected if None)

        Returns:
            List of FileInfo objects
        """
        # Auto-detect default branch if not provided
        if branch is None:
            branch = self.api_client.get_default_branch(owner, repo)
            print(f"📌 Auto-detected branch: {branch}")

        # Fetch repository tree
        tree_data = self.api_client.get_repository_tree(owner, repo, branch)

        # Check if tree was truncated (too large)
        if tree_data.get("truncated", False):
            print("⚠️  Warning: Repository tree was truncated (too large)")

        # Process tree items
        files = []
        for item in tree_data.get("tree", []):
            # Only process files (blobs), skip directories (trees)
            if item["type"] == "blob":
                raw_url = f"{self.api_client.BASE_RAW_URL}/{owner}/{repo}/refs/heads/{branch}/{item['path']}"

                file_info = FileInfo(
                    path=item["path"],
                    raw_url=raw_url,
                    size=item.get("size", 0),
                    type=item["type"]
                )
                files.append(file_info)

        return files


class TreeNode:
    """Node in the directory tree structure"""

    def __init__(self, name: str, is_file: bool = False, file_info: Optional[FileInfo] = None):
        """
        Initialize tree node

        Args:
            name: Node name (directory or filename)
            is_file: True if this is a file node
            file_info: FileInfo object if this is a file
        """
        self.name = name
        self.is_file = is_file
        self.file_info = file_info
        self.children = {}

    def add_path(self, path_parts: List[str], file_info: FileInfo):
        """
        Add a file path to the tree

        Args:
            path_parts: List of path components
            file_info: FileInfo object for the file
        """
        if not path_parts:
            return

        current_part = path_parts[0]

        if len(path_parts) == 1:
            # This is a file (leaf node)
            self.children[current_part] = TreeNode(
                current_part, is_file=True, file_info=file_info)
        else:
            # This is a directory
            if current_part not in self.children:
                self.children[current_part] = TreeNode(
                    current_part, is_file=False)

            self.children[current_part].add_path(path_parts[1:], file_info)

    def render(self, prefix: str = "", is_last: bool = True) -> List[str]:
        """
        Render tree structure as ASCII art with URLs

        Args:
            prefix: Current line prefix for indentation
            is_last: Whether this is the last child in parent

        Returns:
            List of formatted lines
        """
        lines = []

        # Determine the connector and next prefix
        connector = "└── " if is_last else "├── "
        extension = "    " if is_last else "│   "

        if self.is_file:
            # File node with URL
            lines.append(f"{prefix}{connector}{self.name}")
            url_prefix = prefix + extension
            lines.append(f"{url_prefix}→ {self.file_info.raw_url}")
        else:
            # Directory node
            if self.name:  # Skip root name
                lines.append(f"{prefix}{connector}{self.name}/")

            # Render children
            sorted_children = sorted(
                self.children.items(), key=lambda x: (x[1].is_file, x[0]))

            for i, (child_name, child_node) in enumerate(sorted_children):
                is_last_child = (i == len(sorted_children) - 1)
                next_prefix = prefix + extension if self.name else prefix
                lines.extend(child_node.render(next_prefix, is_last_child))

        return lines


class MarkdownGenerator:
    """Generates markdown documentation from file information"""

    def __init__(self, files: List[FileInfo], repo_name: str):
        """
        Initialize markdown generator

        Args:
            files: List of FileInfo objects
            repo_name: Repository name for title
        """
        self.files = files
        self.repo_name = repo_name

    def _group_by_directory(self) -> Dict[str, List[FileInfo]]:
        """
        Group files by directory

        Returns:
            Dictionary mapping directory paths to file lists
        """
        directories = {}

        for file in self.files:
            dir_path = file.directory

            if dir_path not in directories:
                directories[dir_path] = []

            directories[dir_path].append(file)

        return directories

    def _calculate_statistics(self) -> Dict[str, int]:
        """
        Calculate repository statistics

        Returns:
            Dictionary with statistics
        """
        total_size = sum(file.size for file in self.files)

        extensions = {}
        for file in self.files:
            ext = file.extension or "no extension"
            extensions[ext] = extensions.get(ext, 0) + 1

        return {
            "total_files": len(self.files),
            "total_size": total_size,
            "extensions": extensions
        }

    def _format_size(self, size_bytes: int) -> str:
        """
        Format file size in human-readable format

        Args:
            size_bytes: Size in bytes

        Returns:
            Formatted size string
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def _build_tree_structure(self) -> TreeNode:
        """
        Build tree structure from file list

        Returns:
            Root TreeNode
        """
        root = TreeNode(self.repo_name, is_file=False)

        for file in self.files:
            path_parts = file.path.split("/")
            root.add_path(path_parts, file)

        return root

    def _generate_statistics_section(self, f, stats: Dict):
        """Generate statistics section"""
        f.write("## 📊 Repository Statistics\n\n")
        f.write(f"- **Total Files:** {stats['total_files']}\n")
        f.write(
            f"- **Total Size:** {self._format_size(stats['total_size'])}\n")
        f.write(f"- **File Types:**\n")

        # Sort by count descending
        sorted_extensions = sorted(
            stats['extensions'].items(), key=lambda x: x[1], reverse=True)
        for ext, count in sorted_extensions[:10]:  # Top 10 extensions
            f.write(f"  - `{ext}`: {count} files\n")

        if len(stats['extensions']) > 10:
            f.write(f"  - ... and {len(stats['extensions']) - 10} more\n")

        f.write("\n---\n\n")

    def _generate_tree_view_section(self, f, root: TreeNode):
        """Generate tree view section with inline URLs"""
        f.write("## 🌳 Project Structure (Tree View)\n\n")
        f.write(
            "Visual tree structure with raw GitHub URLs for direct file access.\n\n")
        f.write("```\n")

        # Render tree
        tree_lines = root.render(prefix="", is_last=True)
        for line in tree_lines:
            f.write(line + "\n")

        f.write("```\n\n")
        f.write("---\n\n")

    def _generate_quick_reference_section(self, f):
        """Generate quick reference table"""
        f.write("## 📋 Quick Reference Index\n\n")
        f.write("Alphabetical listing of all files with direct URLs.\n\n")
        f.write("| File Path | Raw URL |\n")
        f.write("|-----------|----------|\n")

        # Sort files alphabetically by path
        sorted_files = sorted(self.files, key=lambda x: x.path)

        for file in sorted_files:
            # Escape pipes in path if any
            escaped_path = file.path.replace("|", "\\|")
            f.write(f"| `{escaped_path}` | {file.raw_url} |\n")

        f.write("\n---\n\n")

    def _generate_detailed_listings_section(self, f, directories: Dict[str, List[FileInfo]]):
        """Generate detailed file listings grouped by directory"""
        f.write("## 📁 Detailed File Listings\n\n")
        f.write("Comprehensive file information organized by directory.\n\n")

        for dir_path in sorted(directories.keys()):
            # Directory header
            f.write(f"### 📂 {dir_path}\n\n")

            # Sort files alphabetically
            sorted_files = sorted(
                directories[dir_path], key=lambda x: x.filename)

            for file in sorted_files:
                f.write(f"#### `{file.filename}`\n\n")
                f.write(f"- **Full Path:** `{file.path}`\n")
                f.write(f"- **Size:** {self._format_size(file.size)}\n")
                f.write(f"- **Extension:** `{file.extension or 'none'}`\n")
                f.write(f"- **Raw URL:**\n")
                f.write(f"  ```\n")
                f.write(f"  {file.raw_url}\n")
                f.write(f"  ```\n\n")

            f.write("\n")

    def generate(self, output_file: str):
        """
        Generate complete markdown file map with all sections

        Args:
            output_file: Output filename
        """
        directories = self._group_by_directory()
        stats = self._calculate_statistics()
        tree_root = self._build_tree_structure()

        with open(output_file, "w", encoding="utf-8") as f:
            # Header
            f.write(f"# {self.repo_name} - File Access Map\n\n")
            f.write(
                "**Professional file map with raw GitHub URLs for AI assistants and developers.**\n\n")
            f.write(
                "This document provides three complementary views of the repository structure:\n")
            f.write("1. **Statistics** - Overview of repository contents\n")
            f.write("2. **Tree View** - Visual hierarchy with inline URLs\n")
            f.write("3. **Quick Reference** - Alphabetical table for fast lookup\n")
            f.write("4. **Detailed Listings** - Comprehensive file information\n\n")
            f.write("---\n\n")

            # Section 1: Statistics
            self._generate_statistics_section(f, stats)

            # Section 2: Tree View
            self._generate_tree_view_section(f, tree_root)

            # Section 3: Quick Reference
            self._generate_quick_reference_section(f)

            # Section 4: Detailed Listings
            self._generate_detailed_listings_section(f, directories)

            # Footer
            f.write("---\n\n")
            f.write("## 📝 Document Information\n\n")
            f.write(f"- **Generated by:** GitHub Repository File Map Generator\n")
            f.write(f"- **Repository:** {self.repo_name}\n")
            f.write(f"- **Total Files:** {stats['total_files']}\n")
            f.write(
                f"- **Total Size:** {self._format_size(stats['total_size'])}\n\n")
            f.write(
                "**Note:** This file map is auto-generated. URLs point to raw file contents on GitHub.\n")


class FileMapGenerator:
    """Main orchestrator for file map generation"""

    def __init__(self, token: Optional[str] = None):
        """
        Initialize file map generator

        Args:
            token: Optional GitHub personal access token
        """
        self.api_client = GitHubAPIClient(token)
        self.analyzer = RepositoryAnalyzer(self.api_client)

    def generate(
        self,
        owner: str,
        repo: str,
        branch: Optional[str] = None,
        output_file: str = "FILE_MAP.md"
    ):
        """
        Generate file map for a repository

        Args:
            owner: GitHub username or organization
            repo: Repository name
            branch: Branch name (auto-detected if None)
            output_file: Output markdown filename
        """
        print(f"🚀 Starting file map generation for {owner}/{repo}")
        print("=" * 60)

        # Check rate limit
        try:
            rate_limit = self.api_client.check_rate_limit()
            core_limit = rate_limit["resources"]["core"]
            print(
                f"📊 API Rate Limit: {core_limit['remaining']}/{core_limit['limit']}")
            print(f"   Resets at: {core_limit['reset']}")
            print()
        except Exception as e:
            print(f"⚠️  Could not check rate limit: {e}")
            print()

        # Analyze repository
        print(f"🔍 Fetching repository tree...")
        try:
            files = self.analyzer.analyze(owner, repo, branch)
            print(f"✅ Found {len(files)} files\n")
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP Error: {e}")
            print(f"   Status Code: {e.response.status_code}")
            print(f"   Response: {e.response.text}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error during analysis: {e}")
            sys.exit(1)

        # Generate markdown
        print(f"📝 Generating markdown file map...")
        print(f"   - Statistics section")
        print(f"   - Tree view with URLs")
        print(f"   - Quick reference table")
        print(f"   - Detailed listings")
        print()

        try:
            generator = MarkdownGenerator(files, repo)
            generator.generate(output_file)
            print(f"✅ File map created: {output_file}\n")
        except Exception as e:
            print(f"❌ Error generating markdown: {e}")
            sys.exit(1)

        print("=" * 60)
        print("✨ File map generation complete!")


def main():
    """Main execution function"""

    # Configuration
    # Set to your token or None for unauthenticated
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", None)
    OWNER = "momchilantonov"
    REPO = "CraftForgeStudio"
    BRANCH = None  # None = auto-detect default branch
    OUTPUT_FILE = "README_REPOSITORY_FILE_MAP.md"

    # Create generator and run
    generator = FileMapGenerator(token=GITHUB_TOKEN)

    try:
        generator.generate(
            owner=OWNER,
            repo=REPO,
            branch=BRANCH,
            output_file=OUTPUT_FILE
        )
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
