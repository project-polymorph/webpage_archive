#!/usr/bin/env node

const cheerio = require('cheerio');
const fs = require('fs');
const path = require('path');

// Load configuration
function loadConfig() {
    // Try to load config from environment variable first
    const configEnvPath = process.env.HTML_CLEANER_CONFIG;
    const defaultConfigPath = path.join(__dirname, 'scripts/cleaner/configs/default.json');
    
    let configPath = configEnvPath || defaultConfigPath;
    try {
        if (!fs.existsSync(configPath)) {
            console.warn(`Config file not found at ${configPath}, falling back to default config`);
            configPath = defaultConfigPath;
        }
        
        const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
        console.log(`Loaded config from: ${configPath}`);
        return config;
    } catch (error) {
        console.error(`Error loading config file: ${error.message}`);
        process.exit(1);
    }
}

const config = loadConfig();

function cleanHTML(htmlContent) {
    const $ = cheerio.load(htmlContent);

    // Remove all matched elements using config
    config.selectorsToRemove.forEach(selector => {
        $(selector).remove();
    });

    // Handle base64 images
    $('img[src^="data:image"]').each(function() {
        const $img = $(this);
        // Option 1: Remove base64 images completely
        if (config.removeBase64Images) {
            $img.remove();
        }
        // Option 2: Replace with placeholder
        else if (config.replaceBase64WithPlaceholder) {
            $img.attr('src', 'placeholder.jpg');
        }
    });

    // Remove empty paragraphs and divs
    $('p:empty, div:empty').remove();

    // Remove all HTML comments
    $('*').contents().each(function () {
        if (this.type === 'comment') {
            $(this).remove();
        }
    });

    // Remove configured attributes
    $('*').each(function() {
        const element = $(this);
        config.attributesToRemove.forEach(attr => {
            element.removeAttr(attr);
        });
    });

    // Enhanced empty element cleaning
    $('*').each(function () {
        const $el = $(this);
        // Skip if element is an image or contains an image
        if ($el.is('img') || $el.find('img').length > 0) {
            return;
        }
        // Remove if element is empty or only contains whitespace/newlines
        if (!$el.text().trim() && !$el.find('video').length) {
            $el.remove();
        }
    });

    return $.html();
}

function processFile(inputPath, outputDir) {
    try {
        // Check if input file exists
        if (!fs.existsSync(inputPath)) {
            console.error(`Error: Input file "${inputPath}" does not exist`);
            return;
        }

        // Check if file is HTML
        if (!inputPath.toLowerCase().endsWith('.html')) {
            console.error(`Error: File "${inputPath}" is not an HTML file`);
            return;
        }

        // Create output directory if it doesn't exist
        if (!fs.existsSync(outputDir)) {
            fs.mkdirSync(outputDir, { recursive: true });
        }

        // Generate output filename maintaining the same name
        const fileName = path.basename(inputPath);
        const outputPath = path.join(outputDir, fileName);

        // Skip if output file already exists
        if (fs.existsSync(outputPath)) {
            console.log(`Skipping: ${fileName} (already exists in destination)`);
            return;
        }

        // Read the file
        const htmlContent = fs.readFileSync(inputPath, 'utf8');

        // Clean the HTML
        const cleanedHTML = cleanHTML(htmlContent);

        // Write the cleaned HTML to specified output file
        fs.writeFileSync(outputPath, cleanedHTML);
        console.log(`Successfully cleaned HTML. Saved to: ${outputPath}`);

    } catch (error) {
        console.error(`Error processing file: ${error.message}`);
    }
}

// Handle command line arguments
const args = process.argv.slice(2);

if (args.length !== 2) {
    console.log(`
Usage: clean-cheerio <input.html> <output_dir>
    
Example: clean-cheerio input.html output_directory
    
This will clean the HTML file and save it to the specified output directory
with the same filename
    `);
} else {
    processFile(args[0], args[1]);
}