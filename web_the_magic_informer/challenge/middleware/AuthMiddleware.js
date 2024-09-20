import { decode } from "../helpers/JWTHelper.js";

const AuthMiddleware = async (req, res, next) => {
    try{
        if (req.cookies.session === undefined) {
            if(!req.is('application/json')) return res.redirect('/');
            return res.status(401).json({ status: 'unauthorized', message: 'Authentication required!' });
        }
        return decode(req.cookies.session)
            .then(user => {
                req.user = user;
                return next();
            })
            .catch((e) => {
                console.log(e);
                res.redirect('/logout');
            });
    } catch(e) {
        console.log(e);
        return res.redirect('/logout');
    }
}

export { AuthMiddleware };