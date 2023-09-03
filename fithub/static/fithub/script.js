document.addEventListener('DOMContentLoaded', function(){
    document.querySelector('#profile').addEventListener('click', function(){
        document.querySelector('#profile-view').style.opacity = '100%';
        document.querySelector('#profile-view').style.width = '600px';
        document.querySelector('#profile-view').style.height = '550px';
        document.querySelector('#food').style.opacity = '30%';
        document.querySelector('#weight').style.opacity = '30%';
        document.querySelectorAll('#profile-view > *').forEach( element => {
            element.style.display = 'block';
        });
        
        let age = document.querySelector('#profile-info p:nth-child(2)').textContent;
        if (age[0] === '0'){
            let profile_info = document.querySelector('#profile-info');
            let nutritional_info = document.querySelector('#nutritional-info');
            profile_info.style.display = 'none';
            nutritional_info.style.display = 'none';
            document.querySelector('#edit-profile').style.display = 'flex';
        }
    })
    document.querySelector('#profile-view svg').addEventListener('click', function(){
        document.querySelectorAll('#profile-view > *').forEach( element => {
            element.style.display = 'none';
        });
        document.querySelector('#profile-view').style.opacity = '0';
        document.querySelector('#profile-view').style.width = '0';
        document.querySelector('#food').style.opacity = '100%';
        document.querySelector('#weight').style.opacity = '100%';
    })
    
    document.querySelector('#profile-info button').addEventListener('click', function(){
        let profile_info = document.querySelector('#profile-info');

        let age = profile_info.querySelector('p:nth-child(2)').textContent[0];

        let nutritional_info = document.querySelector('#nutritional-info');
        profile_info.style.display = 'none';
        nutritional_info.style.display = 'none';
        document.querySelector('#edit-profile').style.display = 'flex';

    })

    document.querySelector('#edit-profile button').addEventListener('click', function(){
        let user_id = document.querySelector("input[name='user_id']").value;

        console.log(user_id);

        let gender = document.querySelector("select[name='gender']").value;
        let age = document.querySelector("input[name='age']").value;
        let height = document.querySelector("input[name='height']").value;
        let starting_weight = document.querySelector("input[name='starting_weight']").value;
        let csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;

        fetch('edit_profile/' + String(user_id), {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                gender: gender,
                age: age,
                height: height,
                starting_weight: starting_weight   
            })
        }).then(response => {
            if (response.status == 204){
                let profile_info = document.querySelector('#profile-info');
                let nutritional_info = document.querySelector('#nutritional-info');
                profile_info.style.display = 'block';
                nutritional_info.style.display = 'grid';
                document.querySelector('#edit-profile').style.display = 'none';

                console.log('abc')

                document.querySelector('#profile-info p:nth-child(1)').innerHTML = gender[0].toUpperCase() + gender.slice(1);
                document.querySelector('#profile-info p:nth-child(2)').innerHTML = `${age} years old`;
                document.querySelector('#profile-info p:nth-child(3)').innerHTML = `Height: <span> ${height} m </span>`;
                document.querySelector('#profile-info p:nth-child(4)').innerHTML = `Starting weight: <span>${starting_weight} kg </span>`;
                document.querySelector('#profile-info p:nth-child(5)').innerHTML = `Current weight: <span>${starting_weight} kg </span>`;
            }
        })

        
    })
})