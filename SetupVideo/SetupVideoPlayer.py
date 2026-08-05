import os
import sys
from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt, QUrl
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)


class ModernVideoPlayer(QWidget):

  def __init__(self, video_name="SetupVideo.mp4"):
    super().__init__()

    self.setWindowTitle("Video Setup Video / JarChecker")
    self.resize(960, 560)
    self.setMouseTracking(True)

    self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: #f8fafc;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel#TitleLabel {
                font-size: 15px;
                font-weight: bold;
                color: #38bdf8;
                background-color: rgba(15, 23, 42, 0.75);
                padding: 8px 15px;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
            }
            QPushButton {
                background-color: #1e293b;
                color: #f8fafc;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 6px 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #334155;
                border-color: #38bdf8;
            }
            QPushButton:pressed {
                background-color: #0ea5e9;
            }
            QSlider::groove:horizontal {
                border: none;
                height: 6px;
                background: #334155;
                border-radius: 3px;
            }
            QSlider::sub-page:horizontal {
                background: #0ea5e9;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #f8fafc;
                border: 2px solid #0ea5e9;
                width: 14px;
                height: 14px;
                margin: -4px 0;
                border-radius: 7px;
            }
            QSlider::handle:horizontal:hover {
                background: #38bdf8;
            }
        """)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    self.video_path = os.path.join(script_dir, video_name)

    if not os.path.exists(self.video_path):
      print(f"Ошибка: Файл '{video_name}' не найден в папке: {script_dir}")
      sys.exit(1)

    # Главный макет (используем сетку или наложение через Layout, чтобы видео было на фоне)
    main_layout = QVBoxLayout(self)
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.setSpacing(0)

    # Виджет для вывода видео (на весь экран)
    self.video_widget = QVideoWidget(self)
    self.video_widget.setAspectRatioMode(Qt.IgnoreAspectRatio)
    self.video_widget.setMouseTracking(True)
    main_layout.addWidget(self.video_widget)

    # Верхняя надпись (поверх видео, по центру сверху)
    self.title_label = QLabel("Video Setup Video / JarChecker", self.video_widget)
    self.title_label.setObjectName("TitleLabel")
    self.title_label.adjustSize()
    self.title_label.move(20, 0)  # Сверху слева с небольшим отступом

    # Нижняя панель управления (плавающая поверх видео)
    self.control_widget = QWidget(self.video_widget)
    self.control_widget.setStyleSheet(
        "background-color: rgba(15, 23, 42, 0.85); border-top: 1px solid"
        " #334155; border-top-left-radius: 12px; border-top-right-radius: 12px;"
    )
    control_layout = QHBoxLayout(self.control_widget)
    control_layout.setContentsMargins(15, 12, 15, 12)
    control_layout.setSpacing(12)

    # Кнопка Play/Pause
    self.play_button = QPushButton("Пауза", self.control_widget)
    self.play_button.setFixedWidth(100)
    self.play_button.setFixedHeight(34)
    self.play_button.clicked.connect(self.toggle_play)
    control_layout.addWidget(self.play_button)

    # Метка времени
    self.time_label = QLabel("00:00 / 00:00", self.control_widget)
    self.time_label.setStyleSheet("color: #94a3b8; font-size: 12px;")
    control_layout.addWidget(self.time_label)

    # Ползунок прогресса
    self.position_slider = QSlider(Qt.Horizontal, self.control_widget)
    self.position_slider.setRange(0, 0)
    self.position_slider.sliderMoved.connect(self.set_position)
    control_layout.addWidget(self.position_slider)

    # Кнопка звука
    self.mute_button = QPushButton("🔊", self.control_widget)
    self.mute_button.setFixedWidth(45)
    self.mute_button.setFixedHeight(34)
    self.mute_button.clicked.connect(self.toggle_mute)
    control_layout.addWidget(self.mute_button)

    # Ползунок громкости
    self.volume_slider = QSlider(Qt.Horizontal, self.control_widget)
    self.volume_slider.setRange(0, 100)
    self.volume_slider.setValue(100)
    self.volume_slider.setFixedWidth(90)
    self.volume_slider.valueChanged.connect(self.set_volume)
    control_layout.addWidget(self.volume_slider)

    # Анимация для плавной панели управления
    self.anim = QPropertyAnimation(self.control_widget, b"geometry")
    self.anim.setDuration(250)  # Длительность анимации в мс
    self.anim.setEasingCurve(QEasingCurve.OutCubic)

    # Плеер
    self.media_player = QMediaPlayer(self)
    self.audio_output = QAudioOutput(self)
    self.media_player.setAudioOutput(self.audio_output)
    self.media_player.setVideoOutput(self.video_widget)

    self.media_player.positionChanged.connect(self.position_changed)
    self.media_player.durationChanged.connect(self.duration_changed)

    self.media_player.setSource(QUrl.fromLocalFile(self.video_path))
    self.audio_output.setVolume(1.0)
    self.media_player.play()

  def resizeEvent(self, event):
    super().resizeEvent(event)
    # Позиционируем панель снизу при изменении размера окна
    panel_height = 70
    self.control_widget.setGeometry(
        0, self.height(), self.width(), panel_height
    )

  def mouseMoveEvent(self, event):
    panel_height = 70
    # Если мышь в нижней части окна (в пределах 120 пикселей от низа)
    if event.y() >= self.height() - 120:
      self.show_controls()
    else:
      self.hide_controls()
    super().mouseMoveEvent(event)

  def show_controls(self):
    panel_height = 70
    self.anim.stop()
    self.anim.setStartValue(self.control_widget.geometry())
    self.anim.setEndValue(
        QRect(0, self.height() - panel_height, self.width(), panel_height)
    )
    self.anim.start()

  def hide_controls(self):
    panel_height = 70
    self.anim.stop()
    self.anim.setStartValue(self.control_widget.geometry())
    self.anim.setEndValue(
        QRect(0, self.height(), self.width(), panel_height)
    )  # уезжает за нижний край
    self.anim.start()

  def toggle_play(self):
    if (
        self.media_player.playbackState()
        == QMediaPlayer.PlaybackState.PlayingState
    ):
      self.media_player.pause()
      self.play_button.setText("Старт")
    else:
      self.media_player.play()
      self.play_button.setText("Пауза")

  def position_changed(self, position):
    self.position_slider.setValue(position)
    self.update_time_label(position, self.media_player.duration())

  def duration_changed(self, duration):
    self.position_slider.setRange(0, duration)
    self.update_time_label(self.media_player.position(), duration)

  def set_position(self, position):
    self.media_player.setPosition(position)

  def set_volume(self, value):
    self.audio_output.setVolume(value / 100.0)
    if value == 0:
      self.mute_button.setText("🔇")
    else:
      self.mute_button.setText("🔊")

  def toggle_mute(self):
    if self.audio_output.isMuted():
      self.audio_output.setMuted(False)
      self.mute_button.setText("🔊")
    else:
      self.audio_output.setMuted(True)
      self.mute_button.setText("🔇")

  def update_time_label(self, position, duration):
    pos_sec = int(position / 1000)
    dur_sec = int(duration / 1000)

    pos_min = pos_sec // 60
    pos_sec = pos_sec % 60
    dur_min = dur_sec // 60
    dur_sec = dur_sec % 60

    self.time_label.setText(
        f"{pos_min:02d}:{pos_sec:02d} / {dur_min:02d}:{dur_sec:02d}"
    )


# Импорт QRect, который забыли подключить в начале
from PySide6.QtCore import QRect

if __name__ == "__main__":
  app = QApplication(sys.argv)
  player = ModernVideoPlayer(video_name="SetupVideo.mp4")
  player.show()
  sys.exit(app.exec())