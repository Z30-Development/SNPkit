from snpkit.core.discord_ext.webhook import Webhook, Embed, Colour, File

wh = Webhook("https://discord.com/api/webhooks/1517082358044557316/4cAKKh825EvRTJFXea9tkiZOoFXfTw-fhc4lSB5sE6acK-84FNff73REc4i2ddmL-PSG", username="Status-Bot")

wh("Server is online!")

embed = Embed(title="Deploy #42", description="Successful!", color=Colour.green())

embed.set_author("CI/CD", icon_url="https://example.com/icon.png")
embed.set_footer("github.com/Z30-Development/SNPkit")
embed.set_thumbnail("https://example.com/thumb.png")
embed.add_field("Branch", "main", inline=True)
embed.add_field("Duration", "1m 23s", inline=True)
embed.set_image("https://example.com/banner.png")

wh.send("New Deploy:", embed=embed)

wh.send(embeds=[Embed(title="Log"), Embed(title="Metrics")], files=[File("./assets/report.pdf"), File("./assets/Screenshot.png", spoiler=True)],)