import os
import threading
import customtkinter as ctk
from tkinter import filedialog
from yt_dlp import YoutubeDL


# Configuração da aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class YouTubeDownloader(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Configuração da janela
        self.title("YouTube Downloader")
        self.geometry("700x500")
        self.resizable(False, False)

        self.pasta_destino = os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        )

        # Título
        self.titulo = ctk.CTkLabel(
            self,
            text="YouTube Downloader",
            font=ctk.CTkFont(
                size=32,
                weight="bold"
            )
        )
        self.titulo.pack(
            pady=(35, 5)
        )

        # Subtítulo
        self.subtitulo = ctk.CTkLabel(
            self,
            text="Cole o link do vídeo e faça o download",
            font=ctk.CTkFont(
                size=16
            ),
            text_color="gray"
        )
        self.subtitulo.pack(
            pady=(0, 25)
        )

        # Campo do link
        self.link = ctk.CTkEntry(
            self,
            width=580,
            height=50,
            placeholder_text="Cole aqui o link do YouTube...",
            font=ctk.CTkFont(
                size=15
            )
        )
        self.link.pack(
            pady=10
        )

        # Escolha do formato
        self.formato = ctk.CTkOptionMenu(
            self,
            width=250,
            height=42,
            values=[
                "Vídeo MP4",
                "Somente áudio MP3"
            ]
        )
        self.formato.pack(
            pady=15
        )

        # Botão da pasta
        self.botao_pasta = ctk.CTkButton(
            self,
            text="📁 Escolher pasta",
            width=250,
            height=42,
            command=self.escolher_pasta
        )
        self.botao_pasta.pack(
            pady=8
        )

        # Texto da pasta
        self.texto_pasta = ctk.CTkLabel(
            self,
            text=f"Pasta: {self.pasta_destino}",
            font=ctk.CTkFont(
                size=12
            ),
            text_color="gray"
        )
        self.texto_pasta.pack(
            pady=5
        )

        # Botão de download
        self.botao_download = ctk.CTkButton(
            self,
            text="⬇ BAIXAR",
            width=300,
            height=55,
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            command=self.iniciar_download
        )
        self.botao_download.pack(
            pady=25
        )

        # Status
        self.status = ctk.CTkLabel(
            self,
            text="Aguardando o link...",
            font=ctk.CTkFont(
                size=14
            )
        )
        self.status.pack()

    def escolher_pasta(self):

        pasta = filedialog.askdirectory()

        if pasta:
            self.pasta_destino = pasta

            self.texto_pasta.configure(
                text=f"Pasta: {pasta}"
            )

    def iniciar_download(self):

        url = self.link.get().strip()

        if not url:
            self.status.configure(
                text="⚠ Cole um link do YouTube.",
                text_color="orange"
            )
            return

        self.botao_download.configure(
            state="disabled",
            text="BAIXANDO..."
        )

        self.status.configure(
            text="Preparando o download...",
            text_color="#4da6ff"
        )

        thread = threading.Thread(
            target=self.baixar_video,
            args=(url,),
            daemon=True
        )

        thread.start()

    def baixar_video(self, url):

        try:

            tipo = self.formato.get()

            if tipo == "Vídeo MP4":

                configuracao = {
                    "format": (
                        "bestvideo[ext=mp4]"
                        "+bestaudio[ext=m4a]"
                        "/best[ext=mp4]"
                        "/best"
                    ),

                    "outtmpl": (
                        f"{self.pasta_destino}"
                        "/%(title)s.%(ext)s"
                    ),

                    "merge_output_format": "mp4",

                    "progress_hooks": [
                        self.progresso
                    ]
                }

            else:

                configuracao = {
                    "format": "bestaudio/best",

                    "outtmpl": (
                        f"{self.pasta_destino}"
                        "/%(title)s.%(ext)s"
                    ),

                    "postprocessors": [
                        {
                            "key":
                            "FFmpegExtractAudio",

                            "preferredcodec":
                            "mp3",

                            "preferredquality":
                            "192"
                        }
                    ],

                    "progress_hooks": [
                        self.progresso
                    ]
                }

            with YoutubeDL(
                configuracao
            ) as ydl:

                ydl.download([url])

            self.status.configure(
                text="✅ Download concluído!",
                text_color="#40c057"
            )

        except Exception as erro:

            self.status.configure(
                text=(
                    "❌ Erro ao baixar. "
                    "Verifique o link."
                ),
                text_color="#ff4d4d"
            )

            print(
                "Erro:",
                erro
            )

        finally:

            self.botao_download.configure(
                state="normal",
                text="⬇ BAIXAR"
            )

    def progresso(self, dados):

        if dados["status"] == "downloading":

            porcentagem = (
                dados.get(
                    "_percent_str",
                    "0%"
                )
                .strip()
            )

            self.status.configure(
                text=(
                    f"⬇ Baixando: "
                    f"{porcentagem}"
                ),
                text_color="#4da6ff"
            )

        elif dados["status"] == "finished":

            self.status.configure(
                text="Finalizando arquivo...",
                text_color="#4da6ff"
            )


if __name__ == "__main__":

    aplicativo = YouTubeDownloader()

    aplicativo.mainloop()
