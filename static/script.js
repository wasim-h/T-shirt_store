document.addEventListener('DOMContentLoaded', function() {
    
    const form = document.getElementById('queryForm');
    
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const question = document.getElementById('question').value;
            const loading = document.getElementById('loading');
            const resultContainer = document.getElementById('resultContainer');
            const errorContainer = document.getElementById('errorContainer');
            const submitBtn = document.getElementById('submitBtn');

            loading.classList.remove('hidden');
            resultContainer.classList.add('hidden');
            errorContainer.classList.add('hidden');
            submitBtn.disabled = true;

            try {
                const formData = new FormData();
                formData.append('question', question);

                const response = await fetch('/get_answer', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                loading.classList.add('hidden');
                submitBtn.disabled = false;

                if (response.ok) {
                    document.getElementById('answerText').textContent = data.answer;
                    document.getElementById('sqlText').textContent = data.sql_query;
                    resultContainer.classList.remove('hidden');
                } else {
                    errorContainer.textContent = "Error: " + (data.error || "Unknown error occurred");
                    errorContainer.classList.remove('hidden');
                }

            } catch (error) {
                loading.classList.add('hidden');
                submitBtn.disabled = false;
                errorContainer.textContent = "Network Error: " + error.message;
                errorContainer.classList.remove('hidden');
            }
        });
    }
});