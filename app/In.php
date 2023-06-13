<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class In extends Model
{
    protected $fillable = ['app_id','data','ip'];
}
