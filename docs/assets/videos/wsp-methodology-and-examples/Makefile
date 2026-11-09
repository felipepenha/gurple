SKILL_DIR := ../../../../.agents/skills/manim-skill
TOOLS_DIR := $(SKILL_DIR)/tools
VOICE := am_michael
KOKORO_SPEED := 1.22
SCENES := Scene1_WSPMethodology Scene2_ModelWeightPoisoning Scene3_AggressivePruning Scene4_KnowledgeInjection Scene5_SafeguardAbliteration Scene6_Conclusion
OUT_VIDEO := ../wsp-methodology-and-examples.mp4

.PHONY: help tts lint render mux all view clean

help:
	@echo "WSP Methodology & 4 Blog Examples — Manim Video Pipeline"
	@echo ""
	@echo "  make tts     - Generate voiceover.mp3 and timestamps.json (Kokoro voice: $(VOICE))"
	@echo "  make lint    - Verify subcaption and animation timings against timestamps.json"
	@echo "  make render  - Render all 6 3Blue1Brown-style Manim scenes"
	@echo "  make mux     - Concatenate scenes and mux with voiceover into $(OUT_VIDEO)"
	@echo "  make all     - Run tts -> lint -> render -> mux"
	@echo "  make view    - Launch interactive chapter & subtitle viewer"
	@echo "  make clean   - Remove intermediate media/ and temporary files"

tts:
	KOKORO_SPEED="$(KOKORO_SPEED)" uv run --project "$(SKILL_DIR)" python "$(TOOLS_DIR)/tts-generate.py" --narration narration.txt --voice "$(VOICE)"

lint:
	uv run --project "$(SKILL_DIR)" python "$(TOOLS_DIR)/lint-subtitles.py" script.py

render: lint
	uv run --project "$(SKILL_DIR)" manim script.py $(SCENES)

mux:
	ffmpeg -y -f concat -safe 0 -i concat.txt -c copy -movflags +faststart video_silent.mp4
	ffmpeg -y -i video_silent.mp4 -i voiceover.mp3 -filter_complex "[1:a]apad[a]" -map 0:v:0 -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart video.mp4
	cp video.mp4 $(OUT_VIDEO)

all: tts lint render mux

view:
	python3 "$(TOOLS_DIR)/video_viewer.py" $(OUT_VIDEO) --order concat.txt --script script.py

clean:
	rm -rf media video_silent.mp4 __pycache__
