import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  usernameValid:string = localStorage.getItem('username')

  logout() {
    localStorage.removeItem('username')
    window.open('/',"_self")
  }
}
