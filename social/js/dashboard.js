// Dashboard AJAX for follow/like
document.addEventListener('DOMContentLoaded', function() {
    // Handle follow/unfollow
    document.querySelectorAll('.follow-form').forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            const url = this.action;
            const csrf = this.querySelector('[name=csrfmiddlewaretoken]').value;
            const btn = this.querySelector('.icon-follow');
            const action = btn.classList.contains('unfollow') ? 'unfollow' : 'follow';
            
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrf,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({})
            });
            
            if (response.ok) {
                // Toggle button style
                if (action === 'follow') {
                    btn.classList.add('unfollow');
                    btn.innerHTML = '<i class="fas fa-user-minus"></i>';
                    btn.title = 'Unfollow';
                } else {
                    btn.classList.remove('unfollow');
                    btn.innerHTML = '<i class="fas fa-user-plus"></i>';
                    btn.title = 'Follow';
                }
                // Update follower count in the same row (optional)
                const row = this.closest('tr');
                const followerCell = row.querySelector('.follower-count');
                if (followerCell) {
                    let count = parseInt(followerCell.innerText);
                    followerCell.innerText = action === 'follow' ? count + 1 : count - 1;
                }
            }
        });
    });
    
    // Handle like/unlike
    document.querySelectorAll('.like-form').forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            const url = this.action;
            const csrf = this.querySelector('[name=csrfmiddlewaretoken]').value;
            const btn = this.querySelector('.icon-like');
            const action = btn.classList.contains('unlike') ? 'unlike' : 'like';
            
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrf,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({})
            });
            
            if (response.ok) {
                if (action === 'like') {
                    btn.classList.add('unlike');
                    btn.innerHTML = '<i class="fas fa-heart-broken"></i>';
                    btn.title = 'Unlike';
                } else {
                    btn.classList.remove('unlike');
                    btn.innerHTML = '<i class="fas fa-heart"></i>';
                    btn.title = 'Like';
                }
                // Update likes received count
                const row = this.closest('tr');
                const likesCell = row.querySelector('.likes-count');
                if (likesCell) {
                    let count = parseInt(likesCell.innerText);
                    likesCell.innerText = action === 'like' ? count + 1 : count - 1;
                }
            }
        });
    });
});