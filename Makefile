SHELL := /bin/bash

export PATH := /usr/local/opt/ruby/bin:/usr/local/lib/ruby/gems/4.0.0/bin:$(PATH)
export CXX := /usr/local/opt/llvm/bin/clang++
export CC := /usr/local/opt/llvm/bin/clang

.PHONY: install serve build clean new deploy status

## install: Install Ruby dependencies
install:
	bundle install

## serve: Start local dev server at http://localhost:4000
serve:
	bundle exec jekyll serve --watch

## build: Build the site into _site/
build:
	bundle exec jekyll build

## clean: Remove generated site and caches
clean:
	bundle exec jekyll clean

## new: Create a new post (usage: make new title="My Post Title")
new:
	@test -n "$(title)" || (echo "Usage: make new title=\"My Post Title\"" && exit 1)
	@slug=$$(echo "$(title)" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-'); \
	file="_posts/$$(date +%Y-%m-%d)-$$slug.markdown"; \
	echo "---" > "$$file"; \
	echo "layout: post" >> "$$file"; \
	echo "title:  \"$(title)\"" >> "$$file"; \
	echo "date:   $$(date +%Y-%m-%d) $$(date +%H:%M:%S) +0530" >> "$$file"; \
	echo "categories: " >> "$$file"; \
	echo "---" >> "$$file"; \
	echo "" >> "$$file"; \
	echo "Created $$file"

## deploy: Commit and push to GitHub Pages
deploy:
	git add -A
	git commit -m "Update site"
	git push origin main

## status: Check GitHub Pages deployment status
status:
	gh run list --repo aalavandhan/aalavandhan.github.io --limit 5

## help: Show this help
help:
	@grep -E '^## ' Makefile | sed 's/## //' | column -t -s ':'
