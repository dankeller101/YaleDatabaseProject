
import React from 'react';

export default function CsrfToken() {
  let token = document.getElementsByTagName('meta')._csrf.getAttribute('content');
  return <input type='hidden' name='csrfmiddlewaretoken' value={token} />
}