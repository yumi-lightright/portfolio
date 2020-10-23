const quiz = [
  {
    question: '鬼滅の刃のヒロインの名前は？',
    answers: [ '竈門ねずこ', '珠世', '胡蝶しのぶ', '甘露寺蜜璃'],
    correct: '竈門ねずこ'
  }, {
    question: '２０１６年１０月１６日公開の映画「鬼滅の刃」のサブタイトルはなに？',
    answers: [ '有限の定理', '天空の飛行機', '無限列車', '方舟'],
    correct: '無限列車'
  }, {
    question: 'むきむきしているのに女顔の鬼狩りの剣士の名前は？',
    answers: [ '伊黒小芭内', '嘴平伊之助', '吾妻善逸', '富岡義勇'],
    correct: '嘴平伊之助'
  }
];

const $window = window;
const $doc = document;
const $question = $doc.getElementById('js-question');
const $buttons = $doc.querySelectorAll('.btn');

const quizLen = quiz.length;
let quizCount = 0;
let score = 0;

const init = () => {
  $question.textContent = quiz[quizCount].question;
  
  const buttonLen = $buttons.length;
  let btnIndex = 0;
  
  while(btnIndex < buttonLen){
    $buttons[btnIndex].textContent = quiz[quizCount].answers[btnIndex];
    btnIndex++;
  }
};

const goToNext = () => {
  quizCount++;
  if(quizCount < quizLen){
    init(quizCount);
  } else {
    // $window.alert('クイズ終了！');
    showEnd();
  }
};

const judge = (elm) => {
  if(elm.textContent === quiz[quizCount].correct){
    $window.alert('正解!');
    score++;
  } else {
    $window.alert('不正解!');
  }
  goToNext();
};

const showEnd = () => {
  $question.textContent = '終了！あなたの鬼滅マニア度は' + score + '/' + quizLen + 'です';
  
  const $items = $doc.getElementById('js-items');
  $items.style.visibility = 'hidden';
};

init();

let answersIndex = 0;
let answersLen = quiz[quizCount].answers.length;

while(answersIndex < answersLen){
  $buttons[answersIndex].addEventListener('click', (e) => {
    judge(e.target);
  });
  answersIndex++;
}
