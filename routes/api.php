<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\In;
use App\Tasks;
use App\Out;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

Route::get('tellMe', function () {
    // If the Content-Type and Accept headers are set to 'application/json', 
    // this will return a JSON structure. This will be cleaned up later.
    return In::all();
});

Route::get('tellMe/{id}', function($id) {
    return In::where('app_id', '=', $id)->get();
});

// Route::post('main', function(Request $request) {
//     $data = $request->all();
//     return In::create([
//         'ip' => $data['ip'],
//         'data' => $data['data'],
//     ]);
// });

// Route::post('main', function(Request $request) {
//     $data = $request->all();
//     return In::create([
//         'ip' => $data['ip'],
//         'data' => $data['data'],
//     ]);
// });

Route::post('sup/{app_id}', function (Request $request) {
    $data = $request->all();
    In::create([
        'app_id' => $request->app_id,
        'ip' => $data['ip'],
        'data' => $data['data'],
    ]);
    return Tasks::where('app_id', '=', $request->app_id)
        ->where('status','=', 'Pending')->get();
});

Route::post('tryingToAssignTask/{app_id}/{id}', function ($app_id, $id) {
    Tasks::where('app_id', '=', $app_id)
            ->where('id','=', $id)
            ->where('status', '=', 'Pending')
            ->update([
                     'status' =>'Caught'
                    ]); 
});

Route::get('whatsTheOrder/{app_id}/{id}/', function ($app_id,$id) {
    $tasks = Tasks::where('app_id', '=', $app_id)->where('id','=',$id)
    ->where('status', '=', 'Caught')->get();
    Tasks::where('id', '=', $id)->update([
        'status' =>'Assigned'
    ]);
    return $tasks; 
});

Route::post('letMeTellYou', function (Request $request) {
    $data = $request->all();
    return Tasks::create([
        'app_id' => $data['app_id'],
        'type' => $data['type'],
        'payload' => $data['payload'],
        'status' => 'Pending'
    ]);
});

Route::post('beenThereDoneThat', function (Request $request) {
    $data = $request->all();
    Tasks::where('id', '=', $data['id'])->where('app_id','=',$data['app_id'])->update([
        'status' => 'Done'
    ]);
    return Out::create([
        'task_id' => $data['id'],
        'out' => $data['out']
    ]);
});
Route::post('beenThereButfailedThat', function (Request $request) {
    $data = $request->all();
    Tasks::where('id', '=', $data['id'])->where('app_id','=',$data['app_id'])->update([
        'status' => 'Failed'
    ]);
    return Out::create([
        'task_id' => $data['id'],
        'out' => $data['out']
    ]);
});
// Route::put('main/{id}', function(Request $request, $id) {
//     $main = In::findOrFail($id);
//     $main->update($request->all());

//     return $main;
// });

// Route::delete('main/{id}', function($id) {
//     In::find($id)->delete();

//     return 204;
// });