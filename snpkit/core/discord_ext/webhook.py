from __future__ import annotations
from pathlib import Path
from typing import Union
from discord_webhook import DiscordWebhook, DiscordEmbed


class File:
    def __init__(self, path: Union[str, Path], filename: str = None, *, spoiler: bool = False) -> None:
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"File not found: {self.path}")
        self.filename = filename or self.path.name
        if spoiler and not self.filename.startswith("SPOILER_"):
            self.filename = f"SPOILER_{self.filename}"

    def _read(self) -> tuple[str, bytes]:
        return self.filename, self.path.read_bytes()


class Colour:
    def __init__(self, value: Union[str, int]) -> None:
        if isinstance(value, int):
            self._hex = f"{value:06X}"
        elif isinstance(value, str):
            self._hex = value.lstrip("#").upper().zfill(6)
        else:
            raise TypeError("value must be str or int.")

    def __str__(self) -> str:
        return self._hex

    def __repr__(self) -> str:
        return f"Colour('{self._hex}')"

    @classmethod
    def blurple(cls) -> "Colour":
        return cls("5865F2")

    @classmethod
    def green(cls) -> "Colour":
        return cls("57F287")

    @classmethod
    def yellow(cls) -> "Colour":
        return cls("FEE75C")

    @classmethod
    def red(cls) -> "Colour":
        return cls("ED4245")

    @classmethod
    def og_blurple(cls) -> "Colour":
        return cls("7289DA")

    @classmethod
    def dark_theme(cls) -> "Colour":
        return cls("36393F")

    @classmethod
    def white(cls) -> "Colour":
        return cls("FFFFFF")

    @classmethod
    def black(cls) -> "Colour":
        return cls("000000")

    @classmethod
    def from_rgb(cls, r: int, g: int, b: int) -> "Colour":
        for name, val in (("r", r), ("g", g), ("b", b)):
            if not 0 <= val <= 255:
                raise ValueError(f"{name} must be between 0 and 255.")
        return cls(f"{r:02X}{g:02X}{b:02X}")


Color = Colour


class EmbedField:
    def __init__(self, name: str, value: str, *, inline: bool = False) -> None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must not be empty.")
        if not isinstance(value, str) or not value.strip():
            raise ValueError("value must not be empty.")
        self.name = name
        self.value = value
        self.inline = inline


class EmbedAuthor:
    def __init__(self, name: str, *, url: str = None, icon_url: str = None) -> None:
        self.name = name
        self.url = url
        self.icon_url = icon_url


class EmbedFooter:
    def __init__(self, text: str, *, icon_url: str = None) -> None:
        self.text = text
        self.icon_url = icon_url


class Embed:
    def __init__(self, *, title: str = None, description: str = None, color: Union["Colour", str, int] = None, colour: Union["Colour", str, int] = None, url: str = None, timestamp: str = None) -> None:
        self.title = title
        self.description = description
        self.url = url
        self.timestamp = timestamp
        raw_color = colour or color
        if raw_color is None:
            self._color: str = Colour.blurple()._hex
        elif isinstance(raw_color, Colour):
            self._color = raw_color._hex
        else:
            self._color = Colour(raw_color)._hex
        self._fields: list[EmbedField] = []
        self._author: EmbedAuthor = None
        self._footer: EmbedFooter = None
        self._image_url: str = None
        self._thumbnail_url: str = None

    def set_author(self, name: str, *, url: str = None, icon_url: str = None) -> "Embed":
        self._author = EmbedAuthor(name, url=url, icon_url=icon_url)
        return self

    def set_footer(self, text: str, *, icon_url: str = None) -> "Embed":
        self._footer = EmbedFooter(text, icon_url=icon_url)
        return self

    def set_image(self, url: str) -> "Embed":
        self._image_url = url
        return self

    def set_thumbnail(self, url: str) -> "Embed":
        self._thumbnail_url = url
        return self

    def add_field(self, name: str, value: str, *, inline: bool = False) -> "Embed":
        self._fields.append(EmbedField(name, value, inline=inline))
        return self

    def clear_fields(self) -> "Embed":
        self._fields.clear()
        return self

    def _to_discord_embed(self) -> DiscordEmbed:
        de = DiscordEmbed(title=self.title, description=self.description, color=self._color, url=self.url)
        if self.timestamp:
            de.set_timestamp(self.timestamp)
        if self._author:
            de.set_author(name=self._author.name, url=self._author.url, icon_url=self._author.icon_url)
        if self._footer:
            de.set_footer(text=self._footer.text, icon_url=self._footer.icon_url)
        if self._image_url:
            de.set_image(url=self._image_url)
        if self._thumbnail_url:
            de.set_thumbnail(url=self._thumbnail_url)
        for field in self._fields:
            de.add_embed_field(name=field.name, value=field.value, inline=field.inline)
        return de


class Webhook:
    _VALID_PREFIX = "https://discord.com/api/webhooks/"

    def __init__(self, url: str, *, username: str = None, avatar_url: str = None) -> None:
        if not isinstance(url, str) or not url.strip():
            raise ValueError("url must be a non-empty string.")
        if not url.startswith(self._VALID_PREFIX):
            raise ValueError(f"Invalid Discord webhook URL. Must start with '{self._VALID_PREFIX}'.")
        self._url = url
        self._default_username = username
        self._default_avatar_url = avatar_url

    def send(self, content: str = None, *, username: str = None, avatar_url: str = None, tts: bool = False, embed: "Embed" = None, embeds: list["Embed"] = None, file: "File" = None, files: list["File"] = None) -> bool:
        all_embeds: list[Embed] = []
        if embed is not None:
            if not isinstance(embed, Embed):
                raise TypeError("embed must be an Embed object.")
            all_embeds.append(embed)
        if embeds is not None:
            if not isinstance(embeds, list):
                raise TypeError("embeds must be a list.")
            for i, e in enumerate(embeds):
                if not isinstance(e, Embed):
                    raise TypeError(f"embeds[{i}] must be an Embed object, not {type(e).__name__}.")
            all_embeds.extend(embeds)
        if len(all_embeds) > 10:
            raise ValueError("Discord allows a maximum of 10 embeds per message.")
        all_files: list[File] = []
        if file is not None:
            if not isinstance(file, File):
                raise TypeError("file must be a File object.")
            all_files.append(file)
        if files is not None:
            if not isinstance(files, list):
                raise TypeError("files must be a list.")
            for i, f in enumerate(files):
                if not isinstance(f, File):
                    raise TypeError(f"files[{i}] must be a File object, not {type(f).__name__}.")
            all_files.extend(files)
        if content is None and not all_embeds and not all_files:
            raise ValueError("At least one of content, embed/embeds, or file/files must be provided.")
        wh = DiscordWebhook(url=self._url, content=content, username=username or self._default_username, avatar_url=avatar_url or self._default_avatar_url, tts=tts)
        for e in all_embeds:
            wh.add_embed(e._to_discord_embed())
        for f in all_files:
            name, data = f._read()
            wh.add_file(file=data, filename=name)
        try:
            response = wh.execute()
        except Exception as exc:
            raise ConnectionError(f"Failed to send webhook: {exc}") from exc
        if response.status_code not in (200, 204):
            raise ConnectionError(f"Discord returned status {response.status_code}: {response.text}")
        return True

    def __call__(self, content: str, **kwargs) -> bool:
        return self.send(content, **kwargs)