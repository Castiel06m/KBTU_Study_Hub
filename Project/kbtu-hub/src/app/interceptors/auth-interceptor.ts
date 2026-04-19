import { HttpInterceptorFn } from '@angular/common/http';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = localStorage.getItem('access');

  // Список эндпоинтов, которым НЕ нужен токен 
  const excludedUrls = ['/users/register/', '/login/'];
  const isExcluded = excludedUrls.some(url => req.url.includes(url));

  // токен только если он есть И это не запрос на регистрацию/вход
  if (token && !isExcluded) {
    const authReq = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
    return next(authReq);
  }

  return next(req);
};