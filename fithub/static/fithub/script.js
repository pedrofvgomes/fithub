document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#logout').addEventListener('click', function () {
        window.location.href = '/logout';
    })

    document.querySelector('#profile').addEventListener('click', function () {
        document.querySelector('#profile-view').style.opacity = '100%';
        document.querySelector('#profile-view').style.width = '600px';
        document.querySelector('#profile-view').style.height = '550px';
        document.querySelector('#food').style.opacity = '30%';
        document.querySelector('#weight').style.opacity = '30%';
        document.querySelector('#edit-profile').style.display = 'none';
        document.querySelector('#edit-nutrition').style.display = 'none';
        document.querySelector('#profile-info').style.display = 'block';
        document.querySelector('#nutritional-info').style.display = 'grid';
        document.querySelectorAll('#profile-view > *').forEach(element => {
            element.style.display = 'block';
        });

        let user_id = document.querySelector('#profile-info button').id;
        fetch('user/' + String(user_id))
            .then(response => response.json())
            .then(data => {
                age = data.age;
                objective = data.objective;
                if (age == 0) {
                    let profile_info = document.querySelector('#profile-info');
                    let nutritional_info = document.querySelector('#nutritional-info');
                    profile_info.style.display = 'none';
                    nutritional_info.style.display = 'none';
                    document.querySelector('#edit-profile').style.display = 'flex';
                }
                else if (objective === '') {
                    document.querySelector('#nutritional-info').style.display = 'none';
                    document.querySelector('#edit-nutrition').style.display = 'flex';
                    document.querySelector('#edit-nutrition').style.flexDirection = 'column';
                }
            })

        let age = document.querySelector('#profile-info p:nth-child(2)').textContent;
        if (age[0] === '0') {
            let profile_info = document.querySelector('#profile-info');
            let nutritional_info = document.querySelector('#nutritional-info');
            profile_info.style.display = 'none';
            nutritional_info.style.display = 'none';
            document.querySelector('#edit-profile').style.display = 'flex';
        }
    })
    document.querySelector('#profile-view > svg').addEventListener('click', function () {
        document.querySelectorAll('#profile-view > *').forEach(element => {
            element.style.display = 'none';
        });
        document.querySelector('#profile-view').style.opacity = '0';
        document.querySelector('#profile-view').style.width = '0';
        document.querySelector('#profile-view').style.height = '0';
        document.querySelector('#food').style.opacity = '100%';
        document.querySelector('#weight').style.opacity = '100%';
    })

    let clear = document.querySelector('#profile-info button');
    clear.addEventListener('click', function () {
        let user_id = clear.id;

        window.location.href = 'clear/' + user_id;
    })

    document.querySelector('#edit-profile button').addEventListener('click', function () {
        let user_id = document.querySelector("input[name='user_id']").value;

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
            if (response.status == 204) {
                let profile_info = document.querySelector('#profile-info');
                let nutritional_info = document.querySelector('#nutritional-info');
                profile_info.style.display = 'block';
                nutritional_info.style.display = 'grid';
                document.querySelector('#edit-profile').style.display = 'none';

                document.querySelector('#profile-info p:nth-child(1)').innerHTML = gender[0].toUpperCase() + gender.slice(1);
                document.querySelector('#profile-info p:nth-child(2)').innerHTML = `${age} years old`;
                document.querySelector('#profile-info p:nth-child(3)').innerHTML = `Height: <span> ${height} m </span>`;
                document.querySelector('#profile-info p:nth-child(4)').innerHTML = `Starting weight: <span>${starting_weight} kg </span>`;
                document.querySelector('#profile-info p:nth-child(5)').innerHTML = `Current weight: <span>${starting_weight} kg </span>`;

                let user_id = document.querySelector('#profile-info button').id;
                fetch('user/' + String(user_id))
                    .then(response => response.json())
                    .then(data => {
                        objective = data.objective;
                        if (objective === '') {
                            document.querySelector('#nutritional-info').style.display = 'none';
                            document.querySelector('#edit-nutrition').style.display = 'flex';
                            document.querySelector('#edit-nutrition').style.flexDirection = 'column';
                        }
                    })
            }
        })
    });

    document.querySelector('#nutritional-info button').addEventListener('click', function () {
        document.querySelector('#nutritional-info').style.display = 'none';
        document.querySelector('#edit-nutrition').style.display = 'flex';
        document.querySelector('#edit-nutrition').style.flexDirection = 'column';

        let csrfToken = document.querySelector("#edit-nutrition input[name='csrfmiddlewaretoken']").value;
        let user_id = document.querySelector("#edit-nutrition input[name='user_id']").value;
        fetch('user/' + String(user_id), {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
        })
            .then(response => response.json())
            .then(data => {
                document.querySelector('#objective option:first-child').setAttribute('selected', 'false')
                document.querySelectorAll('#objective option').forEach(element => {
                    if (element.textContent === data.objective) {
                        element.setAttribute('selected', 'true');
                    }
                });

                document.querySelector('#activity option:first-child').setAttribute('selected', 'false')
                document.querySelectorAll('#activity option').forEach(element => {
                    if (element.textContent === data.activity) {
                        element.setAttribute('selected', 'true');
                    }
                });
            })

    })
    document.querySelector('#edit-nutrition button').addEventListener('click', function () {
        let csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;

        let user_id = document.querySelector("input[name='user_id']").value;

        let objective_sel = document.querySelector("#objective");
        let objective_text = objective_sel.options[objective_sel.selectedIndex].text;
        let objective = objective_sel.value;
        let activity_sel = document.querySelector("#activity");
        let activity_text = activity_sel.options[activity_sel.selectedIndex].text;
        let activity = activity_sel.value;

        let gender = "";
        let weight = 0.0;
        let height = 0.0;
        let age = 0;

        fetch('user/' + String(user_id), {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
        })
            .then(response => response.json())
            .then(data => {
                gender = data.gender;
                weight = parseFloat(data.current_weight),
                    height = parseFloat(data.height);
                age = parseInt(data.age);

                let bmr = 10 * weight + 625 * height - 5 * age;
                if (gender === 'Male') {
                    bmr += 5;
                }
                else {
                    bmr -= 161;
                }

                let daily_calories = bmr;
                switch (parseInt(activity)) {
                    case 1:
                        daily_calories *= 1.2;
                        break;
                    case 2:
                        daily_calories *= 1.375;
                        break;
                    case 3:
                        daily_calories *= 1.465;
                        break;
                    case 4:
                        daily_calories *= 1.55;
                        break;
                    case 5:
                        daily_calories *= 1.725;
                        break;
                    case 6:
                        daily_calories *= 1.9;
                        break;
                    default:
                        break;
                }
                console.log(daily_calories);
                daily_calories -= (4 - objective) * 250;
                if (objective == 1) daily_calories -= 250;
                if (objective == 7) daily_calories += 250;
                daily_calories = Math.round(daily_calories);
                bmr = Math.round(bmr);

                fetch('edit_nutrition/' + String(user_id), {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({
                        objective: objective_text,
                        activity: activity_text,
                        bmr: bmr,
                        daily_calories: daily_calories
                    })
                }).then(response => {
                    if (response.status == 204) {
                        let profile_info = document.querySelector('#profile-info');
                        let nutritional_info = document.querySelector('#nutritional-info');
                        profile_info.style.display = 'block';
                        nutritional_info.style.display = 'grid';
                        document.querySelector('#edit-nutrition').style.display = 'none';

                        document.querySelector('#nutritional-info div:nth-of-type(1) p:nth-child(2)').textContent = objective_text;
                        document.querySelector('#nutritional-info div:nth-of-type(2) p:nth-child(2)').textContent = String(bmr);
                        document.querySelector('#nutritional-info div:nth-of-type(3) p:nth-child(2)').textContent = activity_text;
                        document.querySelector('#nutritional-info div:nth-of-type(4) p:nth-child(2)').textContent = String(daily_calories);

                        location.reload();
                    }
                })
            })
    })

    document.querySelector('#add-food').addEventListener('click', function () {
        let food_log = document.querySelector('#food-log');

        food_log.style.opacity = '100%';
        food_log.style.width = '600px';
        food_log.style.height = '550px';
        document.querySelector('#food').style.opacity = '30%';
        document.querySelector('#weight').style.opacity = '30%';
        document.querySelectorAll('#food-log  *').forEach(element => {
            element.style.display = 'block';
            if (element.id == 'search' || element.classList.contains('food')) element.style.display = 'flex';
        });
    })

    document.querySelector('#food-log > svg').addEventListener('click', function () {
        document.querySelectorAll('#food-log  *').forEach(element => {
            element.style.display = 'none';
        });
        document.querySelector('#food-log').style.opacity = '0';
        document.querySelector('#food-log').style.width = '0';
        document.querySelector('#food-log').style.height = '0';
        document.querySelector('#food').style.opacity = '100%';
        document.querySelector('#weight').style.opacity = '100%';
    })



    // add food
    let plus = document.querySelectorAll('#search-results > .food > svg');
    plus.forEach(element => {
        element.addEventListener('click', function () {
            let parent = element.parentElement;
            let name = parent.querySelector(' span:nth-child(1)').textContent;
            let weight = parent.querySelector(' span:nth-child(2)').textContent;
            let calories = parent.querySelector(' span:nth-child(3)').textContent;
            let meal_sel = document.querySelector("#meal");
            let meal_text = meal_sel.options[meal_sel.selectedIndex].text;
            let user_id = document.querySelector('#edit-profile input[name="user_id"]').value;
            let csrfToken = document.querySelector("#food-log input[name='csrfmiddlewaretoken']").value;

            console.log(name);

            fetch('/addfood/' + String(user_id), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    name: name,
                    weight: weight,
                    calories: calories,
                    meal : meal_text
                })
            })
            .then(response => response.json())
            .then(status => {
                if(status == 204){
                    console.log('success');
                }
            })
        })
    });


    // remove food
})