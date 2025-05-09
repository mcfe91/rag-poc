import json
from pathlib import Path

from pydantic import BaseModel, Field

from offline import utils

class DocumentMetadata(BaseModel):
    id: str
    url: str
    title: str
    properties: dict

class Document(BaseModel):
    id: str = Field(default_factory=lambda: utils.generate_rand_hex(length=32))
    metadata: DocumentMetadata
    parent_metadata: DocumentMetadata | None = None
    content: str
    content_quality_score: float | None = None
    summary: str | None = None
    child_urls: list[str] = Field(default_factory=list)

    def write(
        self, output_dir: Path, obfuscate: bool = False, also_save_as_txt: bool = False
    ) -> None:
        """Write document data to file, optionally obfuscating sensitive information.

        Args:
            output_dir: Directory path where the files should be written.
            obfuscate: If True, sensitive information will be obfuscated.
            also_save_as_txt: If True, content will also be saved as a text file.
        """

        output_dir.mkdir(parents=True, exist_ok=True)

        if obfuscate:
            self.obfuscate()
        
        json_page = self.model_dump()

        output_file = output_dir / f"{self.id}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(
                json_page,
                f,
                indent=4,
                ensure_ascii=False,
            )
        
        if also_save_as_txt:
            txt_path = output_file.with_suffix(".txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(self.content)

    def obfuscate(self) -> "Document":
        pass
