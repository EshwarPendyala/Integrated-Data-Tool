import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  formData:string;
  loginStatus:string;
  constructor(private http: HttpClient, private router:Router) { }

  onSubmit(form : NgForm){
    this.formData = form.value;
    this.http.post("http://127.0.0.1:5000/validateUser",this.formData).subscribe(
        responseData => {
          this.loginStatus = responseData as string
          if(this.loginStatus['status'] === 'success')
          {
            localStorage.setItem('username',form.value.username)
            //this.router.navigateByUrl('/')
            window.open('/',"_self")
          }
        }
      );
  }
  ngOnInit(): void {
  }

}
