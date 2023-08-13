const watchdog = new CKSource.EditorWatchdog();

window.watchdog = watchdog;

watchdog.setCreator((element, config) => {
	return CKSource.Editor
		.create(element, config)
		.then(editor => {
			return editor;
		});
});

watchdog.setDestructor(editor => {
	return editor.destroy();
});

watchdog.on('error', handleSampleError);

watchdog
	.create(document.querySelector('#id_body'), {
		// Editor configuration.
		extraPlugins: [MyCustomUploadAdapterPlugin],
		removePlugins: ["Markdown","MediaEmbedToolbar"],
		toolbar: {
			items: [
				// 'exportPDF', 'exportWord', '|',
				'findAndReplace', 'selectAll', '|',
				'heading', '|',
				'bold', 'italic', 'strikethrough', 'underline', 'code', 'subscript', 'superscript', 'removeFormat', '|',
				'bulletedList', 'numberedList', 'todoList', '|',
				'outdent', 'indent', '|',
				'undo', 'redo',
				'-',
				'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'highlight', '|',
				'alignment', '|',
				'link', 'insertImage', 'blockQuote', 'insertTable', 'mediaEmbed', 'codeBlock',  '|',
				'specialCharacters', 'horizontalLine', '|',
				'textPartLanguage', '|',
				'sourceEditing'
			],
			shouldNotGroupWhenFull: true
		},
		mediaEmbed: {
			previewsInData : true
		},
		list: {
			properties: {
				styles: true,
				startIndex: true,
				reversed: true
			}
		},
		// https://ckeditor.com/docs/ckeditor5/latest/features/headings.html#configuration
		heading: {
			options: [
				{ model: 'paragraph', title: 'Paragraph', class: 'ck-heading_paragraph' },
				{ model: 'heading1', view: 'h1', title: 'Heading 1', class: 'ck-heading_heading1' },
				{ model: 'heading2', view: 'h2', title: 'Heading 2', class: 'ck-heading_heading2' },
				{ model: 'heading3', view: 'h3', title: 'Heading 3', class: 'ck-heading_heading3' },
				{ model: 'heading4', view: 'h4', title: 'Heading 4', class: 'ck-heading_heading4' },
				{ model: 'heading5', view: 'h5', title: 'Heading 5', class: 'ck-heading_heading5' },
				{ model: 'heading6', view: 'h6', title: 'Heading 6', class: 'ck-heading_heading6' }
			]
		},
		placeholder: 'write here your note',
		fontFamily: {
			options: [
				'default',
				'Arial, Helvetica, sans-serif',
				'Courier New, Courier, monospace',
				'Georgia, serif',
				'Lucida Sans Unicode, Lucida Grande, sans-serif',
				'Tahoma, Geneva, sans-serif',
				'Times New Roman, Times, serif',
				'Trebuchet MS, Helvetica, sans-serif',
				'Verdana, Geneva, sans-serif'
			],
			supportAllValues: true
		},
	
		fontSize: {
			options: [10, 12, 14, 'default', 18, 20, 22],
			supportAllValues: true
		},
		
		htmlSupport: {
			allow: [
				{
					name: /.*/,
					attributes: true,
					classes: true,
					styles: true
				}
			]
		},
	
		link: {
			decorators: {
				addTargetToExternalLinks: true,
				defaultProtocol: 'https://',
				toggleDownloadable: {
					mode: 'manual',
					label: 'Downloadable',
					attributes: {
						download: 'file'
					}
				}
			}
		},
		// https://ckeditor.com/docs/ckeditor5/latest/features/mentions.html#configuration
		
	})
	.catch(handleSampleError);

function handleSampleError(error) {
	const issueUrl = 'https://github.com/ckeditor/ckeditor5/issues';

	const message = [
		'Oops, something went wrong!',
		`Please, report the following error on ${issueUrl} with the build id "8liuvpfml6m4-vlavqnas7pwp" and the error stack trace:`
	].join('\n');

	console.error(message);
	console.error(error);
}


        // ClassicEditor
        //     .create(document.querySelector('.editor'), {
        //         extraPlugins: [MyCustomUploadAdapterPlugin],
        //     })
        //     .then(editor => {
        //         window.editor = editor;
        //     })
        //     .catch(handleSampleError);

        // function handleSampleError(error) {
        //     const issueUrl = 'https://github.com/ckeditor/ckeditor5/issues';

        //     const message = [
        //         'Oops, something went wrong!',
        //         `Please, report the following error on ${issueUrl} with the build id "whukev2e3gl3-85dnmkq82bz1" and the error stack trace:`
        //     ].join('\n');

        //     console.error(message);
        //     console.error(error);
        // }