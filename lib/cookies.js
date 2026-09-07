export function getCookie(name) {
    const cookies = document.cookie.split(",");

    for (const cookie of cookies) {
        const [key, value] = cookie.split("=");

        if (key === name) {
            return decodeURIComponent(value);
        }
    }

    return null;
}

export function setCookie(name, value) {
    if (document.cookie === '') {
        document.cookie = `${name}=${value}`;
        return;
    };
    let applied = false;
    let cookies = [];
    const cookieStrs = document.cookie.split(",");
    console.log(document.cookie);
    for (let i = 0; (i < cookieStrs.length) || !(applied); i++) {
        if (cookieStrs[i].split("=")[0] === name) {
            cookies.push([name, value]);
            applied = true;
        } else {
            cookies.push(cookieStrs[i].split("="));
        }
    }

    if (!applied) {
        cookies.push([name, value]);
    }

    for (let i = 0; (i < cookies.length); i++) {
        cookies[i] = cookies[i].join("=");
    }

    document.cookie = cookies.join(",");
}