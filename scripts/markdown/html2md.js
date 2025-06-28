const fs = require('fs');
const path = require('path');
const TurndownService = require('turndown');

// Initialize turndown
const turndownService = new TurndownService({
  headingStyle: 'atx',
  hr: '---',
  bulletListMarker: '-',
  codeBlockStyle: 'fenced'
});

// Add custom rule for images with data-lazyload
turndownService.addRule('images', {
  filter: 'img',
  replacement: function (content, node) {
    const src = node.getAttribute('data-lazyload') || node.getAttribute('src');
    const alt = node.getAttribute('alt') || '';
    return src ? `![${alt}](${src})` : '';
  }
});

// Get input and output files from command line
const args = process.argv.slice(2);

if (args.length !== 2) {
  console.log(`
Usage: html2md <input.html> <output_dir>
    
Example: html2md input.html output_directory
    
This will convert the HTML file to Markdown format, 
placing it in the output directory with .md extension
  `);
  process.exit(1);
}

const [inputFile, outputDir] = args;

try {
  // Check if input file exists
  if (!fs.existsSync(inputFile)) {
    console.error(`Error: Input file "${inputFile}" does not exist`);
    process.exit(1);
  }

  // Create output directory if it doesn't exist
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // Generate output filename by replacing .html with .md
  const baseName = path.basename(inputFile, '.html');
  const outputFile = path.join(outputDir, `${baseName}.md`);

  // Skip if output file already exists
  if (fs.existsSync(outputFile)) {
    console.log(`Skipping: ${baseName}.md (already exists in destination)`);
    process.exit(0);
  }

  // Read HTML file
  const html = fs.readFileSync(inputFile, 'utf8');
  
  // Convert to markdown
  const markdown = turndownService.turndown(html);
  
  // Write markdown file
  fs.writeFileSync(outputFile, markdown);
  
  console.log(`Successfully converted ${inputFile} to ${outputFile}`);
} catch (err) {
  console.error('Error:', err.message);
  process.exit(1);
}
