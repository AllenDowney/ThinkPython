#!/usr/bin/env python3
"""
Convert O'Reilly format quizzes from Jupyter notebook to QTI 2.1 format for Canvas import.

This script parses quizzes from a Jupyter notebook and converts them to QTI (Question and 
Test Interoperability) format, which can be imported into Canvas and other LMS systems.
"""

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from zipfile import ZipFile
import uuid
from datetime import datetime
import nbformat


class QuizQuestion:
    """Represents a single quiz question."""
    
    def __init__(self, question_text: str, options: List[str], correct_index: int, 
                 rationale: Optional[str] = None, chapter: Optional[str] = None,
                 quiz_type: Optional[str] = None):
        self.question_text = question_text.strip()
        self.options = [opt.strip() for opt in options]
        self.correct_index = correct_index
        self.rationale = rationale.strip() if rationale else None
        self.chapter = chapter
        self.quiz_type = quiz_type  # 'Formative' or 'Summative'
        self.id = str(uuid.uuid4())


class QuizParser:
    """Parses quiz questions from notebook cells."""
    
    def __init__(self):
        self.current_chapter = None
        self.current_quiz_type = None
        
    def parse_notebook(self, notebook_path: str) -> List[QuizQuestion]:
        """Parse all questions from a notebook file."""
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        
        questions = []
        
        for cell in nb.cells:
            if cell.cell_type != 'markdown':
                continue
                
            source = cell.source
            
            # Check for chapter title
            if source.startswith('# Title'):
                match = re.search(r'# Title\s+(.+)', source)
                if match:
                    self.current_chapter = match.group(1).strip()
            
            # Check for quiz type
            if '## Quiz Type' in source:
                match = re.search(r'## Quiz Type\s+(.+)', source)
                if match:
                    self.current_quiz_type = match.group(1).strip()
            
            # Check for question
            if '### Question' in source:
                question = self._parse_question_cell(source)
                if question:
                    questions.append(question)
        
        return questions
    
    def _parse_question_cell(self, cell_text: str) -> Optional[QuizQuestion]:
        """Parse a single question cell."""
        # Extract question text
        question_match = re.search(r'### Question\s+(.+?)(?=\n- \[|### Rationale|$)', 
                                   cell_text, re.DOTALL)
        if not question_match:
            return None
        
        question_text = question_match.group(1).strip()
        
        # Extract options (checkboxes)
        option_pattern = r'- \[([ X])\]\s+(.+?)(?=\n- \[|### Rationale|$)'
        options = []
        correct_index = None
        
        for match in re.finditer(option_pattern, cell_text, re.DOTALL):
            is_correct = match.group(1).strip() == 'X'
            option_text = match.group(2).strip()
            options.append(option_text)
            
            if is_correct:
                correct_index = len(options) - 1
        
        if not options or correct_index is None:
            return None
        
        # Extract rationale
        rationale_match = re.search(r'### Rationale[s]?\s+(.+?)(?=###|$)', 
                                    cell_text, re.DOTALL)
        rationale = rationale_match.group(1).strip() if rationale_match else None
        
        return QuizQuestion(
            question_text=question_text,
            options=options,
            correct_index=correct_index,
            rationale=rationale,
            chapter=self.current_chapter,
            quiz_type=self.current_quiz_type
        )


class QTIGenerator:
    """Generates QTI 2.1 XML files."""
    
    def __init__(self):
        self.namespaces = {
            '': 'http://www.imsglobal.org/xsd/imsqti_v2p1',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
        }
    
    def escape_xml(self, text: str) -> str:
        """Escape XML special characters."""
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&apos;')
        return text
    
    def markdown_to_html(self, text: str) -> str:
        """Convert markdown to HTML for QTI display."""
        # Handle code blocks with backticks (inline code)
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        
        # Handle inline math (basic support) - keep as is for now
        # text = re.sub(r'\$([^$]+)\$', r'<var>\1</var>', text)
        
        # Handle line breaks - preserve structure
        lines = text.split('\n')
        html_lines = []
        for line in lines:
            line = line.strip()
            if line:
                html_lines.append(line)
        
        # Join with breaks, wrap in paragraph
        if html_lines:
            return '<p>' + '<br/>'.join(html_lines) + '</p>'
        return '<p></p>'
    
    def create_assessment_item(self, question: QuizQuestion) -> ET.Element:
        """Create a QTI assessmentItem for a single question."""
        # Register namespaces
        ET.register_namespace('', self.namespaces[''])
        ET.register_namespace('xsi', self.namespaces['xsi'])
        
        # Create root element
        item = ET.Element('assessmentItem', {
            'identifier': question.id,
            'title': f'Question {question.id[:8]}',
            'adaptive': 'false',
            'timeDependent': 'false',
            'xmlns': self.namespaces[''],
            'xsi:schemaLocation': 'http://www.imsglobal.org/xsd/imsqti_v2p1 http://www.imsglobal.org/xsd/qti/qtiv2p1/imsqti_v2p1.xsd'
        })
        
        # Response declaration
        response_declaration = ET.SubElement(item, 'responseDeclaration', {
            'identifier': 'RESPONSE',
            'cardinality': 'single',
            'baseType': 'identifier'
        })
        
        correct_response = ET.SubElement(response_declaration, 'correctResponse')
        correct_value = ET.SubElement(correct_response, 'value')
        correct_value.text = f'OPTION{question.correct_index}'
        
        # Outcome declaration (for scoring)
        outcome_declaration = ET.SubElement(item, 'outcomeDeclaration', {
            'identifier': 'SCORE',
            'cardinality': 'single',
            'baseType': 'float'
        })
        
        default_value = ET.SubElement(outcome_declaration, 'defaultValue')
        value = ET.SubElement(default_value, 'value')
        value.text = '0'
        
        # Item body
        item_body = ET.SubElement(item, 'itemBody')
        
        # Question text
        question_div = ET.SubElement(item_body, 'div', {'class': 'question'})
        
        # Convert markdown to HTML
        question_html = self.markdown_to_html(question.question_text)
        
        # Parse HTML and add to div
        try:
            # Parse the HTML string
            html_elem = ET.fromstring(question_html)
            question_div.append(html_elem)
        except ET.ParseError:
            # Fallback: add as escaped text in paragraph
            question_p = ET.SubElement(question_div, 'p')
            question_p.text = self.escape_xml(question.question_text)
        
        # Choice interaction
        choice_interaction = ET.SubElement(item_body, 'choiceInteraction', {
            'responseIdentifier': 'RESPONSE',
            'shuffle': 'false',
            'maxChoices': '1'
        })
        
        # Add choice options
        for idx, option in enumerate(question.options):
            simple_choice = ET.SubElement(choice_interaction, 'simpleChoice', {
                'identifier': f'OPTION{idx}',
                'fixed': 'false'
            })
            
            # Convert markdown to HTML for options
            option_html = self.markdown_to_html(option)
            try:
                # Parse the HTML string
                html_elem = ET.fromstring(option_html)
                simple_choice.append(html_elem)
            except ET.ParseError:
                # Fallback: add as escaped text
                simple_choice.text = self.escape_xml(option)
        
        # Response processing
        response_processing = ET.SubElement(item, 'responseProcessing')
        response_if = ET.SubElement(response_processing, 'responseIf')
        
        # Condition: if response equals correct response
        response_condition = ET.SubElement(response_if, 'match')
        variable = ET.SubElement(response_condition, 'variable', {'identifier': 'RESPONSE'})
        correct = ET.SubElement(response_condition, 'correct', {'identifier': 'RESPONSE'})
        
        # Then: set score to 1
        set_outcome = ET.SubElement(response_if, 'setOutcomeValue', {'identifier': 'SCORE'})
        base_value = ET.SubElement(set_outcome, 'baseValue', {'baseType': 'float'})
        base_value.text = '1'
        
        # Add feedback if rationale exists
        if question.rationale:
            modal_feedback = ET.SubElement(item, 'modalFeedback', {
                'identifier': 'FEEDBACK',
                'showHide': 'show',
                'outcomeIdentifier': 'FEEDBACK'
            })
            
            feedback_div = ET.SubElement(modal_feedback, 'div', {'class': 'feedback'})
            feedback_p = ET.SubElement(feedback_div, 'p')
            
            rationale_html = self.markdown_to_html(question.rationale)
            try:
                # Parse the HTML string
                html_elem = ET.fromstring(rationale_html)
                feedback_p.append(html_elem)
            except ET.ParseError:
                # Fallback: add as escaped text
                feedback_p.text = self.escape_xml(question.rationale)
        
        return item
    
    def create_manifest(self, questions: List[QuizQuestion], quiz_title: str, output_dir: Path) -> ET.Element:
        """Create IMS manifest file."""
        # Register namespaces for manifest
        ET.register_namespace('', 'http://www.imsglobal.org/xsd/imscp_v1p1')
        ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        
        manifest = ET.Element('manifest', {
            'identifier': str(uuid.uuid4()),
            'xmlns': 'http://www.imsglobal.org/xsd/imscp_v1p1',
            'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsi:schemaLocation': 'http://www.imsglobal.org/xsd/imscp_v1p1 http://www.imsglobal.org/xsd/qti/qtiv2p1/imsqti_v2p1.xsd'
        })
        
        metadata = ET.SubElement(manifest, 'metadata')
        schema = ET.SubElement(metadata, 'schema')
        schema.text = 'QTI Package'
        schemaversion = ET.SubElement(metadata, 'schemaversion')
        schemaversion.text = '2.1'
        
        organizations = ET.SubElement(manifest, 'organizations', {'default': 'TOC1'})
        organization = ET.SubElement(organizations, 'organization', {'identifier': 'TOC1'})
        title = ET.SubElement(organization, 'title')
        title.text = quiz_title
        
        resources = ET.SubElement(manifest, 'resources')
        
        # Add resource for each question
        for question in questions:
            resource = ET.SubElement(resources, 'resource', {
                'identifier': question.id,
                'type': 'imsqti_item_xmlv2p1',
                'href': f'questions/{question.id}.xml'
            })
            file_elem = ET.SubElement(resource, 'file', {'href': f'questions/{question.id}.xml'})
        
        return manifest
    
    def generate_qti_package(self, questions: List[QuizQuestion], quiz_title: str, output_path: Path):
        """Generate complete QTI package as ZIP file."""
        # Create temporary directory structure
        temp_dir = output_path.parent / f'temp_qti_{uuid.uuid4().hex[:8]}'
        temp_dir.mkdir(exist_ok=True)
        questions_dir = temp_dir / 'questions'
        questions_dir.mkdir(exist_ok=True)
        
        try:
            # Generate individual question files
            for question in questions:
                item = self.create_assessment_item(question)
                tree = ET.ElementTree(item)
                question_file = questions_dir / f'{question.id}.xml'
                tree.write(question_file, encoding='utf-8', xml_declaration=True)
            
            # Generate manifest
            manifest = self.create_manifest(questions, quiz_title, temp_dir)
            manifest_tree = ET.ElementTree(manifest)
            manifest_file = temp_dir / 'imsmanifest.xml'
            manifest_tree.write(manifest_file, encoding='utf-8', xml_declaration=True)
            
            # Create ZIP file
            with ZipFile(output_path, 'w') as zipf:
                zipf.write(manifest_file, 'imsmanifest.xml')
                for question_file in questions_dir.glob('*.xml'):
                    zipf.write(question_file, f'questions/{question_file.name}')
        
        finally:
            # Clean up temporary directory
            import shutil
            if temp_dir.exists():
                shutil.rmtree(temp_dir)


def sanitize_filename(name: str) -> str:
    """Convert a string to a safe filename."""
    # Replace spaces and special characters
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '_', name)
    return name


def main():
    """Main conversion function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Convert O\'Reilly format quizzes to QTI format for Canvas import'
    )
    parser.add_argument(
        'input_notebook',
        type=str,
        help='Path to the Jupyter notebook containing quizzes'
    )
    parser.add_argument(
        '-o', '--output-dir',
        type=str,
        default=None,
        help='Output directory for QTI packages (default: quizzes/)'
    )
    
    args = parser.parse_args()
    
    input_path = Path(args.input_notebook)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        return 1
    
    # Create output directory
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = input_path.parent / 'quizzes'
    
    output_dir.mkdir(exist_ok=True)
    
    print(f"Parsing quizzes from: {input_path}")
    parser_obj = QuizParser()
    questions = parser_obj.parse_notebook(str(input_path))
    
    if not questions:
        print("Warning: No questions found in the notebook!")
        return 1
    
    print(f"Found {len(questions)} questions")
    
    # Group by chapter and quiz type
    chapter_groups = {}
    summative_questions = []
    
    for q in questions:
        if q.quiz_type and 'summative' in q.quiz_type.lower():
            summative_questions.append(q)
        else:
            chapter = q.chapter or 'Uncategorized'
            if chapter not in chapter_groups:
                chapter_groups[chapter] = []
            chapter_groups[chapter].append(q)
    
    print("\nQuestions by chapter:")
    for chapter, chapter_questions in sorted(chapter_groups.items()):
        print(f"  {chapter}: {len(chapter_questions)} questions")
    if summative_questions:
        print(f"  Summative: {len(summative_questions)} questions")
    
    generator = QTIGenerator()
    created_packages = []
    
    # Generate QTI package for each chapter
    for chapter, chapter_questions in sorted(chapter_groups.items()):
        if not chapter_questions:
            continue
        
        safe_name = sanitize_filename(chapter)
        output_path = output_dir / f'{safe_name}_qti.zip'
        quiz_title = f'{chapter} - Formative Quiz'
        
        print(f"\nGenerating QTI package: {output_path.name}")
        generator.generate_qti_package(chapter_questions, quiz_title, output_path)
        created_packages.append((output_path, len(chapter_questions)))
    
    # Generate summative quiz package
    if summative_questions:
        output_path = output_dir / 'Summative_Quiz_qti.zip'
        quiz_title = 'Think Python - Summative Quiz'
        
        print(f"\nGenerating QTI package: {output_path.name}")
        generator.generate_qti_package(summative_questions, quiz_title, output_path)
        created_packages.append((output_path, len(summative_questions)))
    
    print(f"\n✓ Created {len(created_packages)} QTI package(s) in: {output_dir}")
    print("\nPackages created:")
    for package_path, count in created_packages:
        print(f"  - {package_path.name} ({count} questions)")
    
    print(f"\nTo import into Canvas:")
    print(f"  1. Go to your Canvas course")
    print(f"  2. Navigate to Settings → Import Course Content")
    print(f"  3. Select 'QTI .zip file' as the content type")
    print(f"  4. Upload each package individually")
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())

