PACKAGE_NAME      := LilyPondRenderer
SUBLIME_PACKAGES  := $(HOME)/Library/Application Support/Sublime Text/Packages
LINK              := $(SUBLIME_PACKAGES)/$(PACKAGE_NAME)
SOURCE            := $(CURDIR)
ZIP               := $(PACKAGE_NAME).sublime-package

.PHONY: help install uninstall reinstall package status clean

help:
	@echo "Targets:"
	@echo "  make install    Symlink this folder into Sublime Text's Packages dir"
	@echo "  make uninstall  Remove the symlink"
	@echo "  make reinstall  uninstall + install"
	@echo "  make package    Build $(ZIP) (zip) for manual install"
	@echo "  make status     Show install state"
	@echo "  make clean      Remove build artefacts"

install:
	@if [ -e "$(LINK)" ] && [ ! -L "$(LINK)" ]; then \
		echo "ERROR: '$(LINK)' exists and is not a symlink."; \
		echo "Move or remove it first, then re-run 'make install'."; \
		exit 1; \
	fi
	@mkdir -p "$(SUBLIME_PACKAGES)"
	@ln -sfn "$(SOURCE)" "$(LINK)"
	@echo "Installed: $(LINK) -> $(SOURCE)"

uninstall:
	@if [ -L "$(LINK)" ]; then \
		rm "$(LINK)"; echo "Removed symlink $(LINK)"; \
	elif [ -e "$(LINK)" ]; then \
		echo "Refusing to delete '$(LINK)' — not a symlink"; exit 1; \
	else \
		echo "Not installed"; \
	fi

reinstall: uninstall install

package: $(ZIP)

$(ZIP): $(wildcard *.py *.sublime-* *.json) Main.sublime-menu README.md LICENSE
	@rm -f "$(ZIP)"
	@zip -r "$(ZIP)" . \
		-x ".git/*" ".gitignore" "Makefile" "*.sublime-package" \
		   "*.pyc" "__pycache__/*" ".DS_Store"
	@echo "Built $(ZIP)"

status:
	@if [ -L "$(LINK)" ]; then \
		printf "Installed (symlink) -> "; readlink "$(LINK)"; \
	elif [ -e "$(LINK)" ]; then \
		echo "Installed at $(LINK) (NOT a symlink)"; \
	else \
		echo "Not installed"; \
	fi

clean:
	@rm -f "$(ZIP)"
	@find . -name __pycache__ -type d -exec rm -rf {} +
	@echo "Cleaned"
