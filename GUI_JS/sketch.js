var p = [];
let img = [];
var first = false;
var obj_spec = [];
var last_spec = 0;
var this_spec = 0;
var generation = 0;
var s = 0;
var m = 0;
var power_max = 5;
var new_spec = [];
var spec = [27, 42, 15, 10, 6, 8, 8, 13, 14, 16, 19, 14, 15, 14, 17, 21, 24, 17, 11, 12, 14, 16, 18, 17, 14, 14, 15, 11, 10, 12, 15, 18,
     13, 13, 11, 11, 12, 6, 6, 7, 8, 8, 10, 10];

function preload(){
p = loadJSON("blades_mod.json");
for (var i = 0; i < 612; i++) {
    img[i] = loadImage('Blade_' + i + '.jpg');
}
pp =loadImage("pp.jpg");

}
function imageLoader(s) {

    img = loadImage('Blade_' + s + '.jpg', imgSuccess, imgFailure);

    return imgSuccess;
}
function imgSuccess() {

    return img;
}
function imgFailure() {
    console.log("loadFailed");

}

function next() {
    first = true;
    generation++;
    //console.log(p.length);

}

function setup(){

    createCanvas(1350, 750);
    angleMode(DEGREES);
    this_spec = spec[0];
    obj_spec = [last_spec, this_spec];

    button = createButton('NEXT GENERATION');
    button.position(600, 550, 150, 40);


}

function draw(){
    background(75);
    //console.log(p[55].power);
        button.mousePressed(next);
    new_spec = show(obj_spec, generation, first);
    obj_spec = new_spec;
    //image(pp, 0, 0, 50, 50);
}
function show(obj_spec, generation) {

    this_spec = obj_spec[1];
    last_spec = obj_spec[0];
    //console.log("in show()");
    s = 0;


    for (var i = generation; i<generation+1; i++) {
        //console.log(generation);

        for (var j = last_spec; j < this_spec; j++) {

            //console.log(this_spec);
            //console.log(last_spec);
            if (p[j].power < power_max) {
                power_max = p[j].power;
                m = j;
                console.log(m);

            }
            fill(100);
            rect(0, 0, 1300, 100);
            top_show();
            push();
            translate(((s)%10)*130, (floor(s/10))*150);
            noFill();

            //noFill();
            //rect(200,200,200,200);
            if (j == m) {
                tint(255, 0, 0);
                rect(0, 100, 125, 125);
                //fill(255, 0, 0);
            }
            else {
                rect(0, 100, 125, 125);
            }

            strokeWeight(2);

            //console.log("print");
            //bezier(p[j].genx[0],p[j].geny[0],p[j].genx[1],p[j].geny[1],/*p[j].genx[2],p[j].geny[2]//,p[j].genx[3],p[j].geny[3],p[j].genx[4],
            //    //p[j].geny[4],*/p[j].genx[5],p[j].geny[5],/*p[j].genx[6],p[j].geny[6],p[j].genx[7],p[j]//.geny[7],*/p[j].genx[8],p[j].geny[8],p[j].genx[9],
            //    p[j].geny[9]);
            //loadedImg = imageLoader(j);
            image(img[j], 0, 100, 125, 125);
            rect(0, 100, 125, 125);
            pop();

            s++;
        }
        if (first == true) {
            last_spec = this_spec;
            this_spec += spec[i+1];

        }
        first = false;

        }

    obj_spec[1] = this_spec;
    obj_spec[0] = last_spec;

    return obj_spec;
}
function top_show() {

    textSize(18);
    fill(255);
    var s = 'VAWT Blade Optimisation using Invasive Weed Optimisation Algorithm';
    text(s, 10, 10, 250, 80);

    var v = 'Maximum Power = '+ str(abs(power_max)) +'W'
    textSize(18);
    fill(255);
    text(v, 1000, 10, 250, 50);

    var u = 'GENERATION = '+ generation;
    textSize(18);
    text(u, 1000, 50, 250, 80);
}
