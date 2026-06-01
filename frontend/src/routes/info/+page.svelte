<script lang="ts">
  const javaCode = `package subcode;
import java.util.*;
import java.io.*;
public class test {
    public static void main (String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[] a = new int[n];
        for (int i = 0; i < n; i++) {
            a[i] = scanner.nextInt();
        }
        long sum = 0;
        for (int i = 0; i < n; i++) {
            sum += a[i];
        }
        System.out.println(sum);
    }
}`;

  const cppCode = `#include <bits/stdc++.h>
using namespace std;

int main() {
    int n; cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
    long long ans = 0;
    for (int i = 0; i < n; i++) {
        ans += a[i];
    }
    cout << ans << "\\n";
}`;

  const pythonCode = `n = int(input())
a = list(map(int, input().split()))
print(sum(a))`;
</script>

<div class="prose prose-invert max-w-3xl mx-auto p-8 rounded-xl shadow-lg text-white">
  <h1 class="text-3xl font-bold mb-4">Intro to CP &amp; In-Houses</h1>
  <p>Competitive programming contests involve competitors submitting a single file (.cpp, .py, .java, etc.) that accepts input and prints output from/to the system. A tutorial on how this would work on <a href="https://codeforces.com" class="text-indigo-400 underline hover:text-indigo-300">codeforces.com</a> is located here. The grader (<a href="https://tjctgrader.org" class="text-indigo-400 underline hover:text-indigo-300">tjctgrader.org</a>) maintained by Computer Team officers functions in a similar manner as the Codeforces contest system.</p>

  <p>We will host contests (in-houses) on our grader website. Some will be rated and others unrated. Rated contests will impact your overall standing that is used to calculate rankings for travel competition team selection to represent TJ. Other variables in the ranking calculation may include USACO division and Codeforces rating. You can see the dates these in-house will occur in the schedule in the public Google Drive.</p>

  <h2 class="text-2xl font-bold mt-8 mb-2">Rankings Formula (2025-2026)</h2>
  <p><strong>Tentative formula is:</strong></p>
  <ul>
    <li>Data is taken from grader website</li>
    <li>Codeforces rating is simply the max rating of your account.</li>
    <li>Each USACO division is mapped to a rating where Bronze/Not Participated → 800, Silver → 1200, Gold → 1600, Platinum → 1900.</li>
    <li>Each user gets a rating for every rated in-house contest, which is <span class="font-mono">1200 · (#participants − rank + 1) / #participants + 800</span>, linearly mapping rank to a rating in the interval (800, 2000]. If you do not participate in the contest, you get a 0.</li>
    <li>Your overall rating for in-houses is the average of all your ratings, with <span class="font-mono">max(0, min(2, #contests − 2))</span> drops. After 3 contests have happened, your overall rating will not include your lowest score and after 4 contests, your overall rating will not include your lowest two scores. Problem setters will get one extra drop for each rated contest they have been an author of.</li>
    <li>Your final index is a <span class="font-mono">0.2, 0.35, 0.45</span> weighted average of USACO, Codeforces, and In-Houses, weighting your higher values more.</li>
    <li>Problemsetters for the first rated contest will have to drop it, so their rating will be a <span class="font-mono">0.4, 0.6</span> weighted average of USACO and Codeforces</li>
  </ul>

  <h2 class="text-2xl font-bold mt-8 mb-2">Travel Competitions</h2>
  <p>The in-person competitions we are very likely to send teams to are Widener, Code Quest, PClassic, UMD HSPC, VCU HSPC, and UVA HSPC. If there are any other contests you think we should attend, let us know. The application forms for these will be posted on Facebook and Discord a few weeks before the competition. Below is additional information on each contest based on past years, which may change. By default, you are not allowed to use electronic tools to do anything besides type code or view documentation and pre-written code is not allowed.</p>

  <h3 class="text-xl font-bold mt-6 mb-2">Widener</h3>
  <ul>
    <li>We send at least 3 teams of 3, one of which is a freshman team. The competition doesn't have an actual online judge, you just run input/output locally through VSCode, Eclipse, etc. on your computer (one per team).</li>
    <li>To submit, you raise your hand and they come to your table, give you one or two inputs as tests, and look to see if the output is correct.</li>
    <li>You only get one submission per problem, plus one other extra submission.</li>
    <li>You are not allowed to access web browsers, the internet, or other electronic devices.</li>
  </ul>

  <h3 class="text-xl font-bold mt-6 mb-2">Code Quest</h3>
  <ul>
    <li>Teams of 3, 4 in-person teams and 4 online teams, one laptop per team, has novice and advanced divisions.</li>
    <li>This is our first year attending, so we don't have specific details on the contest format.</li>
  </ul>

  <h3 class="text-xl font-bold mt-6 mb-2">PClassic</h3>
  <ul>
    <li>One contest in the fall and another in the spring.</li>
    <li>Teams of 4, no limit on number of teams, one laptop per team, has classic and advanced divisions.</li>
    <li>Templates/pre-downloaded code are allowed.</li>
  </ul>

  <h3 class="text-xl font-bold mt-6 mb-2">UMD</h3>
  <ul>
    <li>Teams of 4, we send 1 team. One laptop is provided, and you must use Java.</li>
  </ul>

  <h3 class="text-xl font-bold mt-6 mb-2">VCU</h3>
  <ul>
    <li>Teams of 4, we send 2 teams. Two laptops are provided.</li>
  </ul>

  <h3 class="text-xl font-bold mt-6 mb-2">UVA</h3>
  <ul>
    <li>Teams of 3, we send 3 teams, one of which is a freshman team. One laptop is provided per team.</li>
  </ul>

  <hr class="my-8 border-slate-700" />

  <h1 class="text-3xl font-bold mb-4">2025–2026 TJCT Grader Guide</h1>

  <h2 class="text-2xl font-bold mt-8 mb-2">Verdicts</h2>
  <ul>
    <li><strong>Accepted (AC)</strong> — Congratulations! Your submission passed all our tests.</li>
    <li><strong>Wrong Answer (WA)</strong> — Try again! Your submission failed a test and thus didn't solve the problem correctly. You will not be able to see what the input you failed on was unless it was the first one. Try creating and debugging on edge cases to catch the error!</li>
    <li><strong>Compilation/Runtime Error</strong> — Your code encountered an error. Check the feedback which might provide more detailed comments. This means your code does not follow the rules of the programming language and did something illegal.</li>
    <li><strong>Time Limit Exceeded (TLE)</strong> — Your code was too slow. Try reducing time complexity or optimizing your code. Note that our servers can only run around 10<sup>9</sup> operations a second. The default time limits for problems are 1 second for C++, 2 seconds for Java, and 3 seconds for Python.</li>
    <li><strong>Memory Limit Exceeded (MLE)</strong> — Your code used too much memory. Store less information. The default memory limit is 256 megabytes.</li>
    <li><strong>Running (RN)</strong> — Your code is currently running. Reload the page to check if your code has finished running. If it hasn't finished for a couple minutes, our servers probably encountered an error. Try resubmitting. If that doesn't work, please let us know.</li>
  </ul>

  <h2 class="text-2xl font-bold mt-8 mb-2">Feedback</h2>
  <p>By clicking on the ID of the submission, you can view additional feedback. Feedback is available for the first test.</p>

  <h2 class="text-2xl font-bold mt-8 mb-2">Submissions</h2>
  <p>Your code should take input from standard in (the terminal) and output to standard out (the terminal). This can be done through <code class="bg-zinc-800 px-1 rounded text-cyan-300">cin/cout</code> (C++), <code class="bg-zinc-800 px-1 rounded text-cyan-300">input()</code> (Python), <code class="bg-zinc-800 px-1 rounded text-cyan-300">Scanner</code> (Java). You can use online documentation to figure out the specifics. You should use your own IDE or text editor to code solutions before uploading the file or copying and pasting into the submission page. We recommend using <a href="https://ide.usaco.guide/" target="_blank" class="text-indigo-400 underline hover:text-indigo-300">https://ide.usaco.guide/</a>.</p>
  <p>Java users, make sure you are naming the class <code class="bg-zinc-800 px-1 rounded text-cyan-300">usercode</code>. We encourage you to use Python or C++, though.</p>
  <p>Example code to solve sum the array (for more help, consult <a href="https://usaco.guide/general/input-output" target="_blank" class="text-indigo-400 underline hover:text-indigo-300">usaco.guide/general/input-output</a>):</p>

  <h3 class="text-xl font-bold mt-6 mb-2">Java</h3>
  <pre class="bg-zinc-950 border border-slate-800 rounded p-4 overflow-x-auto text-sm leading-relaxed"><code>{javaCode}</code></pre>

  <h3 class="text-xl font-bold mt-6 mb-2">C++</h3>
  <pre class="bg-zinc-950 border border-slate-800 rounded p-4 overflow-x-auto text-sm leading-relaxed"><code>{cppCode}</code></pre>

  <h3 class="text-xl font-bold mt-6 mb-2">Python</h3>
  <pre class="bg-zinc-950 border border-slate-800 rounded p-4 overflow-x-auto text-sm leading-relaxed"><code>{pythonCode}</code></pre>

  <h2 class="text-2xl font-bold mt-8 mb-2">Standings</h2>
  <p>Standings are determined by your total points, where each problem solved rewards a set amount of points, and ties are broken by penalty. The penalty for each problem is determined by the number of minutes taken to solve it plus 10 minutes for each wrong submission. Your overall penalty is the sum of your penalty for each solved problem. The numbers in the columns for each problem denote the number of submissions taken to solve the problem, and is negative if the participant has not solved the problem.</p>
</div>
