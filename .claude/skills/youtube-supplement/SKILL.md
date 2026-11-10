---
name: youtube-supplement
description: 공부 주제 페이지의 내용을 YouTube 영상(자막 또는 음성)으로 보완해야 할 때 사용한다. 사용자가 영상 링크를 주며 "영상 내용으로 보완해줘", "음성 추출해서 정리해줘"라고 하거나, 새 주제를 만들 때 노션 필기만으로는 내용이 부족해 영상 보완을 요청했을 때 쓴다. 사용자가 요청하지 않으면 쓰지 않는다.
---

# YouTube 영상으로 주제 내용 보완

노션 필기만으로 부족한 설명을 영상에서 보완하는 절차. **사용자가 요청한 경우에만** 한다.

## 원칙
- 영상 내용은 **일반 본문**(`p`, `ul`, `ol`)으로만 넣는다. 사용자 필기(`.note` `[사용자 노트 필기]`)와 질문(`.note.qa`)은 건드리지 않고 섞지 않는다(CLAUDE.md의 표기 형식 규칙).
- 보완이 필요한 부분에만 추가한다. 전사문을 통째로 붙이지 않고, 해당 섹션 주제에 맞는 핵심을 정리한다.
- 영상에서 나온 수치·주장은 "영상에서 언급" 식으로 출처를 밝히고, 발표자가 "추정치"라고 한 것은 그대로 표시한다.
- 영상 전사문 원문을 길게 인용하지 않는다(저작물). 요약·재구성한다.
- 추출한 전사문·오디오는 사이트 폴더 밖(스크래치 폴더)에 두고, 사이트에는 정리한 결과만 반영한다.

## 절차
1. **사용자 확인**: 영상 링크와 보완할 섹션을 확인한다. 도구 설치와 영상 다운로드는 이번에 진행해도 되는지 사용자에게 먼저 묻는다(파일명·출처·대략 크기 포함).
2. **도구 확인**: `yt-dlp`, `ffmpeg`, `faster-whisper`가 있는지 본다. 없으면 설치를 제안한다(이 노트북은 2026-11 기준 모두 미설치, NVIDIA GPU 없음).
   ```bash
   python -m pip install yt-dlp faster-whisper
   winget install --id Gyan.FFmpeg -e
   ```
3. **자막 먼저**: 오디오 다운로드 전에 자막이 있는지 확인한다. 있으면 음성 인식을 건너뛴다(훨씬 빠르고 정확).
   ```bash
   yt-dlp --list-subs "URL"
   yt-dlp --skip-download --write-subs --write-auto-subs --sub-langs "ko.*" --convert-subs srt -o "<scratch>/%(id)s" "URL"
   ```
4. **자막이 없으면 음성 추출 + 인식**:
   ```bash
   yt-dlp -x --audio-format mp3 -o "<scratch>/%(id)s.%(ext)s" "URL"
   ```
   ```python
   from faster_whisper import WhisperModel
   m = WhisperModel("small", device="cpu", compute_type="int8")   # 정확도가 부족하면 "medium"
   segs, _ = m.transcribe(path, language="ko", vad_filter=True)
   ```
   CPU 전용이라 느리다. 20~30분 영상은 모델에 따라 영상 길이 이상 걸릴 수 있으니 백그라운드로 돌리고, 시작 전에 예상 시간을 사용자에게 알린다.
5. **정리·반영**: 전사문에서 보완할 섹션과 관련된 내용만 골라 본문 형식으로 정리해 해당 `topics/<id>/index.html`에 넣는다. 인식 오류가 의심되는 전문용어(예: 영문 약어, 수치)는 노션 필기·기존 본문과 대조하고, 불확실하면 사용자에게 묻는다.
6. **마무리**: `topics.js`의 `updated`를 갱신하고, CLAUDE.md의 검증 절차(탭·목차·이미지·모바일)를 다시 확인한다.
