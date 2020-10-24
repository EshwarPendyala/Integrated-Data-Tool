import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


@Component({
  selector: 'app-tool',
  templateUrl: './tool.component.html',
  styleUrls: ['./tool.component.css']
})
export class ToolComponent implements OnInit {
  searchText:string = "";
  listOfdatasets:string[];
  columnMetadata:string[];
  tableMetadata:string[];

  constructor(private http: HttpClient) {
    }

  getColumnMetadata(datasetSearch:string){
    this.searchText = datasetSearch;
    this.listOfdatasets = null;
    this.tableMetadata = null;
    this.http.post("http://127.0.0.1:5000/getColumnMetadata",
      {"query":this.searchText, "username":localStorage.getItem('username')}).subscribe(
        responseData => {
          this.columnMetadata = responseData as string[];
        }
      );
  }
  
  getListOfDatasets(){
    this.tableMetadata = null;
    this.columnMetadata = null;
    this.http.post("http://127.0.0.1:5000/getlistofdatasets",
      { "username": localStorage.getItem('username')}).subscribe(
        responseData => {
          this.listOfdatasets = responseData as string[];
        }
      );
  }

  getTableMetadata(datasetSearch: string){
    this.listOfdatasets = null;
    this.columnMetadata = null;
    this.searchText = datasetSearch;
    this.http.post("http://127.0.0.1:5000/tableMetadata",
      { "query": this.searchText, "username": localStorage.getItem('username')}).subscribe(
        responseData => {
          this.tableMetadata = responseData as string[];
        }
      );
  }

  ngOnInit(): void {
    
  }
}
