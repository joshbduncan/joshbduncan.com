---
title: Checking off Linked Records in an Airtable Script
date: 2021-08-03
description: I needed a quick way to check off a bunch of linked records in Airtable so I worked up this little script to do it from an Airtable button.
category: development
tags: airtable, automation, javascript
---

A few years back I built a custom job tracker in [Airtable](https://www.airtable.com/) that helps me keep up with all of my freelance projects. The base is pretty simple and only consists of three tables, "Jobs", "Clients", and "Contacts". As you would expect, each "Job" has a "Client", which in-turn has a "Contact" (some of my clients have multiple contacts).

## Backstory

Previously, I tracked overall time for each project in a "duration" field that I would manually update every time I did any work. And, up until recently non of my time-tracked projects lasted more than week so this method worked just fine... Well, until last month.

See, I bill my clients monthly and some their projects started spanning more than one month, making it hard to determine what I time had already billed when the next month comes around.

To fix this, I created a new table titled "Time Entries" which links back to individual jobs. Every time I work on a project now, I create a new time entry with the date and time that I worked. Each time entry also has a "checkbox" field titled "Invoiced". Now, when the end of the month comes, I can just bill for the time entries that are not checked as "Invoiced".

## The Problem

This new method works well, but I got annoyed today when I had to click off sixty-four linked time entries for one client. I do my invoicing from a custom view in the "Jobs" table so this process takes way too long... You have to click the linked record, scroll down and click the "Invoiced" checkbox, then click out of the linked record pop-up.

I know I could create a filtered view in the "Time Entries" table that's grouped by customer but that's not ideal for me.

## The Solution

I've recently been learning some Javascript and knew Airtable had scripting capabilities so I figured I could whip up something to help me out.

Before I started scripting I switched to my custom "Invoicing" view in the "Jobs" table that I mentioned above. This view only shows jobs with "uninvoiced" time entries and has all records grouped by client so things are easier to see.

To this view, I added a new [button field](https://support.airtable.com/hc/en-us/articles/360048496693-Button-field) that will run my script on the current record when clicked.

## Time to Script

Before I start scripting I like to make a list of everything I'm trying to accomplish. This time the list is short but I find it helps me stay on track...

**Scripting Steps:**

1. Get all time entries for a particular job
2. Loop through all matching time entries
3. Check to make sure the time entry hasn't been invoiced
4. Mark it as invoiced

If you are new to Airtable Scripting like me, here's their [Scripting Documentation](https://www.airtable.com/developers/scripting/api) for reference.

### Getting Setup

First I'll need to get the two tables I'm working with as objects so that I can reference and query them. And, I'll also go ahead and query all of the time entries so I can update the "uninvoiced" ones that match the job I'm invoicing.

```javascript
let jobsTable = base.getTable("Jobs");
let timeEntriesTable = base.getTable("Time Entries");
let timeEntriesQuery = await timeEntriesTable.selectRecordsAsync();
```

I'll be running this script via a button like I mentioned above, but it can also be ran right from the scripting menu so I need to have a way to choose a record in that case.

```javascript
let record = await input.recordAsync("Choose a record", jobsTable);
```

### 1. Get all time entries for a particular job

Airtable makes it easy to get all of the linked entries for a record by getting its cell value. This provides me with a list of each linked record as an object.

```javascript
let linkedTimeEntries = record.getCellValue("Time Entries") || [];
output.text("Found " + linkedTimeEntries.length + " total time entries");
```

### 2. Loop through all matching time entries

Now that I have each linked time entry, I can loop through them and make sure I'm getting the correct info.

```javascript
// loop over all time entries for record
if (linkedTimeEntries.length > 0) {
    for (let i = 0; i < linkedTimeEntries.length; i++) {
        let record = timeEntriesQuery.getRecord(linkedTimeEntries[i].id);
        output.text(record.getCellValue("Date"));
    }
}
```

### 3. Check to make sure the time entry hasn't been invoiced

While looping, I'll need to make sure that each time entry hasn't already been invoiced, If the boolean value of the "Invoiced" field is `false` then I'll output the date of the entry as a check.

```javascript
// loop over all time entries for record
if (linkedTimeEntries.length > 0) {
    for (let i = 0; i < linkedTimeEntries.length; i++) {
        let record = timeEntriesQuery.getRecord(linkedTimeEntries[i].id);
        // if time entry not invoiced
        if (!record.getCellValue("Invoiced")) {
            output.text(record.getCellValue("Date") + " not invoiced");
        }
    }
}
```

### 4. Mark it as invoiced

If a time entry hasn't been "invoiced", I will check it off using the [`updateRecordAsync()`](https://www.airtable.com/developers/scripting/api/table#update-record-async) function.

```javascript
await timeEntriesTable.updateRecordAsync(record.id, {
    Invoiced: true,
});
```

## Putting It All Together

Now that all of the steps I laid out above are covered, I can put everything together and give it a test run.

```javascript
// get the two tables I need to work on
let jobsTable = base.getTable("Jobs");
let timeEntriesTable = base.getTable("Time Entries");
// get all time entries for later reference
let timeEntriesQuery = await timeEntriesTable.selectRecordsAsync();
// when run via button, automatically use that record otherwise choose
let record = await input.recordAsync("Choose a record", jobsTable);
// get all linked time entries for record
let linkedTimeEntries = record.getCellValue("Time Entries") || [];
output.text("Found " + linkedTimeEntries.length + " total time entries");
// loop over all time entries for record
if (linkedTimeEntries.length > 0) {
    for (let i = 0; i < linkedTimeEntries.length; i++) {
        let record = timeEntriesQuery.getRecord(linkedTimeEntries[i].id);
        // if time entry not invoiced
        if (!record.getCellValue("Invoiced")) {
            // check "Invoiced"
            await timeEntriesTable.updateRecordAsync(record.id, {
                Invoiced: true,
            });
            output.text("✅ " + record.getCellValue("Date"));
        }
    }
}
```

If you are trying something similar, I would highly recommend using a copy of your production Airtable base, or at least make a test "job" with test "time entries".

So, here it is in action.

![Airtable Checkbox Script in Action](/static/images/airtable-checkbox-script.gif){: loading="lazy" }

As you can see, when I want to mark all time entries for a job as "invoiced" I just click the big blue button and the script goes to work. #satisfied

[View the full script here](https://gist.github.com/joshbduncan/10b7f448e984e238fdbfa3fc95ebc1e6)
